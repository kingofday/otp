#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import find_packages
from setuptools import setup

setup(
    name='workano-otp-playback',
    version='0.1',
    description='A plugin for otp playback with different type of otp',
    author='Shahrooz Bazrafshan',
    author_email='shahrooz.bazrafshan@gmail.com',
    url='https://workano.com',
    package_data={
        'wazo_calld_otp_request': ['api.yml'],
    },
    entry_points={
        "wazo_calld.plugins":"otp_request_plugin.plugin:Plugin"
     }
)