#!/usr/bin/env python

from distutils.core import setup

setup(
    name='cdu_pins',
    version='1.0',
    description='CDU Backplane Pin Tool',
    author='Mike Stewart',
    author_email='mastewar1@gmail.com',
    url='',
    packages=['cdu_pins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
)
