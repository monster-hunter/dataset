"""
ROS2 launch file for Intel RealSense camera on NVIDIA Jetson Thor.

Problem: On Jetson Thor (ARM architecture), the RealSense color stream defaults to
MJPEG encoding which is not properly supported, resulting in depth images being
received but color images not working.

Fix: Set color_format to 'rgb8' (or 'yuyv' as fallback) to bypass MJPEG decoding.
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare launch arguments
    color_width_arg = DeclareLaunchArgument(
        'color_width', default_value='640',
        description='Color stream width'
    )
    color_height_arg = DeclareLaunchArgument(
        'color_height', default_value='480',
        description='Color stream height'
    )
    color_fps_arg = DeclareLaunchArgument(
        'color_fps', default_value='30',
        description='Color stream FPS'
    )
    # On Jetson Thor (ARM), MJPEG decoding for color is not supported.
    # Use 'rgb8' or 'bgr8' to receive color images correctly.
    color_format_arg = DeclareLaunchArgument(
        'color_format', default_value='rgb8',
        description='Color stream format. Use rgb8 or bgr8 on Jetson (not mjpeg)'
    )
    depth_width_arg = DeclareLaunchArgument(
        'depth_width', default_value='640',
        description='Depth stream width'
    )
    depth_height_arg = DeclareLaunchArgument(
        'depth_height', default_value='480',
        description='Depth stream height'
    )
    depth_fps_arg = DeclareLaunchArgument(
        'depth_fps', default_value='30',
        description='Depth stream FPS'
    )
    enable_color_arg = DeclareLaunchArgument(
        'enable_color', default_value='true',
        description='Enable color stream'
    )
    enable_depth_arg = DeclareLaunchArgument(
        'enable_depth', default_value='true',
        description='Enable depth stream'
    )
    align_depth_arg = DeclareLaunchArgument(
        'align_depth.enable', default_value='true',
        description='Align depth to color'
    )
    camera_name_arg = DeclareLaunchArgument(
        'camera_name', default_value='camera',
        description='Camera node name'
    )
    serial_no_arg = DeclareLaunchArgument(
        'serial_no', default_value='',
        description='Camera serial number (empty = use first available)'
    )

    # Resolve the path to the config file
    config_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..', 'config'
    )
    config_file = os.path.join(config_dir, 'realsense_jetson.yaml')

    realsense_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name=LaunchConfiguration('camera_name'),
        namespace=LaunchConfiguration('camera_name'),
        parameters=[
            config_file,
            {
                'camera_name': LaunchConfiguration('camera_name'),
                'serial_no': LaunchConfiguration('serial_no'),
                'enable_color': LaunchConfiguration('enable_color'),
                'enable_depth': LaunchConfiguration('enable_depth'),
                'color_width': LaunchConfiguration('color_width'),
                'color_height': LaunchConfiguration('color_height'),
                'color_fps': LaunchConfiguration('color_fps'),
                # Key fix: use rgb8 format instead of mjpeg for Jetson Thor ARM support
                'color_format': LaunchConfiguration('color_format'),
                'depth_width': LaunchConfiguration('depth_width'),
                'depth_height': LaunchConfiguration('depth_height'),
                'depth_fps': LaunchConfiguration('depth_fps'),
                'align_depth.enable': LaunchConfiguration('align_depth.enable'),
            }
        ],
        output='screen',
        emulate_tty=True,
    )

    return LaunchDescription([
        color_width_arg,
        color_height_arg,
        color_fps_arg,
        color_format_arg,
        depth_width_arg,
        depth_height_arg,
        depth_fps_arg,
        enable_color_arg,
        enable_depth_arg,
        align_depth_arg,
        camera_name_arg,
        serial_no_arg,
        realsense_node,
    ])
