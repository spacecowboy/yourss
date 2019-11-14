"""
This file is run using `pip3 install -e` to generate yt_api.egg-info folder
so that we can start the applicaton with the .ini file
"""
from setuptools import setup

requires = [
    'pyramid',
    'waitress',
]

setup(
    name='ytapi',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = ytapi:main'
        ]
    }
)