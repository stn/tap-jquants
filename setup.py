#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="tap-jquants",
    version="0.1.2",
    description="Singer.io tap for J-Quants",
    author="Akira Ishino",
    url="https://github.com/stn/tap-jquants",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_jquants"],
    install_requires=["singer-python==5.13.0", "requests==2.28.2", "backoff==1.8.0"],
    entry_points="""
    [console_scripts]
    tap-jquants=tap_jquants:main
    """,
    packages=find_packages(),
    package_data={"tap_jquants": ["schemas/*.json"]},
    include_package_data=True,
)
