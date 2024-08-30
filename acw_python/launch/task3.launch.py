import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
 
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    pkg_dir = get_package_share_directory('acw_python')
    world_file_name = 'environment3.world'
    
    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(pkg_dir, 'models')
    
    world = os.path.join(pkg_dir, 'worlds', world_file_name)
    launch_file_dir = os.path.join(pkg_dir, 'launch')
    
    gazebo = ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', 
            '-s', 'libgazebo_ros_factory.so'],
            output='screen')
   
    spawn_entity = Node(package='acw_python', executable='rover_node',
                       arguments=['rover', 'rover', '-6', '-8', '0', '-1.5707'],
                       output='screen')

    return LaunchDescription([
        gazebo,
        spawn_entity,
    ])

