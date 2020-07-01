cmake_minimum_required(VERSION 3.9.5)
project(turtlebot_description)

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)

install(DIRECTORY robots
        DESTINATION share/turtlebot_description
)
install(DIRECTORY meshes
        DESTINATION share/turtlebot_description
)
install(DIRECTORY test
        DESTINATION share/turtlebot_description
)
install(DIRECTORY urdf
        DESTINATION share/turtlebot_description
)

ament_export_dependencies(urdf)
ament_export_dependencies(xacro)
ament_package()
