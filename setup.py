#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module sets up the package for the lib_off_campus_housing_parser"""

from setuptools import find_packages, setup

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

setup(
    name="lib_off_campus_housing_parser",
    version="0.1.0",
    url="https://github.com/jfuruness/lib_off_campus_housing_parser.git",
    download_url='https://github.com/jfuruness/lib_off_campus_housing_parser.git',
    keywords=['Furuness', 'UConn', 'University of Connecticut',
              'Off Campus', 'Commute', 'Apartment'],
    license="BSD",
    description="Optimizes UConn's off campus housing choices",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'XlsxWriter>=1.1.8',
        'googlemaps>=3.0.2',
        'setuptools>=40.8.0',
        'selenium>=3.141.0',
        'beautifulsoup4>=4.8.1'
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'off_campus_housing = lib_off_campus_housing_parser.__main__:main'
        ]},
)
