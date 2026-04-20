# Copyright 2026 Intelligent Robotics Lab

# This file is part of the project Easy Navigation (EasyNav in short)
# licensed under the GNU General Public License v3.0.
# See <http://www.gnu.org/licenses/> for details.

# Easy Navigation program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os

from ament_index_python.packages import get_package_prefix, get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration, FindExecutable
import launch_ros.descriptions


def generate_launch_description():
    prefix = LaunchConfiguration("prefix", default="")
    pkg_path = get_package_share_directory('easynav_playground_drone')
    install_dir = get_package_prefix('easynav_playground_drone')
    ws_dir = install_dir.split("install")[0]
    sim_path = ws_dir+"src/ThirdParty/worlds/PX4-gazebo-models"
    sitl_path = ws_dir+"src/ThirdParty/robots/drone/PX4-Autopilot"
    
    world = "urjc_excavation"

    sdf_file = os.path.join(sim_path, 'models', 'x500_lidar_3d_front', 'model.sdf')

    # NOTE: Removed empty child_frame_id which was causing TF errors
    # tf = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     arguments = ['--x', '0', '--y', '0', '--z', '0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'world', '--child-frame-id', 'base_link']
    # )

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            sdf_file,
            " ",
            "prefix:=", prefix
        ]
    )
    robot_description_param = launch_ros.descriptions.ParameterValue(robot_description_content, value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        #namespace=robot_id,
        output='screen',
        parameters=[{
          'use_sim_time': True,
          'robot_description': robot_description_param,
          'publish_frequency': 100.0,
          'frame_prefix': '',
        }],
    )

    gazebo_sim = ExecuteProcess(
        cmd=[
            'python3',
            'simulation-gazebo',
            '--world',
            world
        ],
        cwd=sim_path,
        output='screen'
    )

    px4_sitl = ExecuteProcess(
        cmd=[
            'make',
            'px4_sitl',
            'gz_x500_lidar_3d_front'
        ],
        cwd=sitl_path,
        additional_env={
            'PX4_GZ_STANDALONE': '1',
            'PX4_GZ_WORLD': [world, '_world']
        },
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_ros_gz',
        parameters=[
            {
                'config_file': os.path.join(
                    pkg_path, 'config', 'drone_bridge.yaml'
                ),
                'use_sim_time': True,
            }
        ],
        output='screen',
    )

    mavros = ExecuteProcess(
        cmd=[
            'ros2',
            'launch',
            'easynav_playground_drone',
            'px4.launch',
            'fcu_url:=udp://:14540@14557'
        ],
        output='screen'
    )

    roboligo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('roboligo'),
            'launch/'), 'roboligo.launch.py']),
    )

    return LaunchDescription([
        # tf,
        gazebo_sim,
        px4_sitl,
        bridge,
        mavros,
        roboligo,
        # robot_state_publisher_node
    ])

