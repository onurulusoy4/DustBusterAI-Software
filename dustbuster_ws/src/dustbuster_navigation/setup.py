from setuptools import setup

package_name = 'dustbuster_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='onur',
    maintainer_email='onurulusoys4@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'save_map = dustbuster_navigation.save_map:main',
            'explorer = dustbuster_navigation.explorer:main',
            'TSPGeneticSolver = dustbuster_navigation.TSPGeneticSolver:main',
            'WaypointsNavigation = dustbuster_navigation.WaypointsNavigation:main',
        ],
    },
)
