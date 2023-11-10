from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='akshit',
    maintainer_email='akshit@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node_1a = my_robot_controller.my_node:main",
            "circle1 = my_robot_controller.circle1:main",
            "pose_subscriber = my_robot_controller.pose_subscriber:main",
            "turtle_controller = my_robot_controller.turtle_controller:main"
        ],
    },
)
