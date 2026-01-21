from setuptools import find_packages, setup

package_name = 'speaker_driver'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gordon',
    maintainer_email='gordonthecellist@gmail.com',
    description='Driver for walker bot speaker',
    license='None',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'speaker_driver_node = speaker_driver.speaker_driver_node:main'
        ],
    },
)
