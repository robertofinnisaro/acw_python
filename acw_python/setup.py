from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'acw_python'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share/' + package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share/' + package_name, 'models', 'hokuyo'), glob('models/hokuyo/**/*')),
        (os.path.join('share/' + package_name, 'scripts'), glob('scripts/*')),
        (os.path.join('share/' + package_name, 'sdf'), glob('sdf/*')),
        (os.path.join('share/' + package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('share/' + package_name, 'models', 'task3_floor'), glob('models/task3_floor/**/*', recursive=True)),
        (os.path.join('share/' + package_name, 'models', 'task2_floor'), glob('models/task2_floor/**/*', recursive=True)),
        (os.path.join('share/' + package_name, 'models', 'task1_floor'), glob('models/task1_floor/**/*', recursive=True)),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rob',
    maintainer_email='rob@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rover_node = acw_python.rover_node:main'
        ],
    },
)
