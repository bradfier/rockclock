from setuptools import setup

version = '0.1.0'

setup(
    name='Rockclock',
    packages=['rockclock'],
    entry_points={
        "console_scripts": ['rockclock = rockclock.rockclock:main']
    },
    version=version,
    description="Motorsport timer to Rockblock Bridge",
    author="Richard Bradfield",
    author_email="bradfirj@fstab.me",
)
