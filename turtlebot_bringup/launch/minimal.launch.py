from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, TextSubstitution, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    turtlebot_description_path = get_package_share_path('turtlebot_description')
    turtlebot_bringup_path = get_package_share_path('turtlebot_bringup')
    default_model_path = turtlebot_description_path / 'robots/create_circles_rplidar.urdf.xacro'

    default_rviz_config_path = turtlebot_bringup_path / 'rviz/robot.rviz'

    gui_arg = DeclareLaunchArgument(name='gui', default_value='false', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')
    show_rviz_arg = DeclareLaunchArgument(name='show_rviz', default_value='false', choices=['true', 'false'],
                                          description='Flag to enable automatic start of rviz')
    start_teleop_arg = DeclareLaunchArgument(name='teleop', default_value='true', choices=['true', 'false'],
                                             description='Flag to enable joystick teleop')

    #robot_description =

    robot_description = ParameterValue(Command(['xacro ', str(default_model_path)]), value_type=str)
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('rplidar_ros2'),
                'launch',
                'rplidar_launch.py'
            ])
        ]),
        launch_arguments={
            'serial_port': '/dev/rplidar',
            'frame_id': 'laser_frame'
        }.items()
    )

    turtlebot_node = Node(
        package='create_node',
        executable='turtlebot_node',
        parameters=[{'port': '/dev/create',
                     'has_gyro': True}],
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description}],
    )

    # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui')),
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui')),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        condition=IfCondition(LaunchConfiguration('show_rviz')),
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[{'enable_button': use_sim_time, 'robot_description': robot_description}],
        condition=IfCondition(LaunchConfiguration('teleop')),
    )

    teleop_twist_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        parameters=[{'enable_button': 4},
                    {'axis_linear.x': 1},
                    {'axis_angular.yaw': 3}],
        condition=IfCondition(LaunchConfiguration('teleop')),
    )

    return LaunchDescription([
        gui_arg,
        model_arg,
        rviz_arg,
        show_rviz_arg,
        start_teleop_arg,
        turtlebot_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
        joy_node,
        teleop_twist_joy_node,
        rplidar_launch,
    ])
