"""
launch_sim.launch.py

Standalone launch file to run Gazebo, RViz, robot state publisher, joint state publisher, and spawn the robot in the room.

Usage: ros2 launch dustbuster_launch launch_sim.launch.py

Author: Onur Ulusoy
Date: 22.03.2023

This code is licensed under the MIT license.
"""

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    # Get the share directory for dustbuster_launch, gazebo_ros
    pkg_dustbuster_launch = get_package_share_directory('dustbuster_launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Declare world argument
    world_file = os.path.join(pkg_dustbuster_launch, 'worlds', 'room.world')
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=world_file,
        description='Path to world file to load'
    )

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        ),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'verbose': 'false',
            'gui': 'true',
            'headless': 'false',
            'debug': 'false'
        }.items()
    )

    # Robot URDF file path
    robot_urdf_file = os.path.join(pkg_dustbuster_launch, 'urdf', 'dustbuster.urdf')

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        arguments=[robot_urdf_file],
        parameters=[{'use_sim_time': True}],
    )

    # Joint state publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    # Spawn entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'dustbuster', '-x', '0', '-y', '0', '-z', '0.15'],
        output='screen',
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_dustbuster_launch, 'rviz', 'room.rviz')],
        output='screen'
    )

    # Get the config directory
    config_dir = os.path.join(pkg_dustbuster_launch, 'config')

    # Slam launch
    online_async_launch_file = os.path.join(pkg_dustbuster_launch, 'launch', 'online_async_launch.py')
    online_async_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(online_async_launch_file),
        launch_arguments={
            'use_sim_time': 'true',
            'params_file': os.path.join(config_dir, 'mapper_params_online_async.yaml'),
        }.items()
    )

    # Return the launch description
    return LaunchDescription([
        world_arg,
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        rviz,
        online_async_launch
    ])
