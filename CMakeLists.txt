cmake_minimum_required(VERSION 3.20)
project(easynav_playground_drone)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config launch
        DESTINATION share/${PROJECT_NAME})

ament_package()