cmake_minimum_required(VERSION 3.9.5)
project(turtlebot_bringup)

find_package(ament_cmake REQUIRED)

# catkin_add_env_hooks(25.turtlebot SHELLS sh DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)

install(
  PROGRAMS
  scripts/turtlebot_addr.py
  DESTINATION bin
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# install(DIRECTORY param
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
# )

install(DIRECTORY icons
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY interactions
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
