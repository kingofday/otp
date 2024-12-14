#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class MyDriver(object):
    def __init__(self, config):
        self._config = config

    def generate(self):
        return 'Dummy Plugin!'