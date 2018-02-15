#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='mapping',
    version='1.0',
    description='Shows product linking',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    install_requires=[
        'tabler', 'jinja2', 'requests'],
    packages=find_packages(),
    include_package_data=True,
    )
