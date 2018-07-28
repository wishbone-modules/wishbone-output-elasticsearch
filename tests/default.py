#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  default.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gevent import monkey

monkey.patch_all()

from wishbone.actor import ActorConfig
from wishbone_output_elasticsearch import ElasticSearchOut


def test_initialize_default():

    actor_config = ActorConfig(
        "elasticsearch", 100, 1, {}, "", disable_exception_handling=True
    )
    try:
        ElasticSearchOut(actor_config)
    except Exception as e:
        assert False, e
    else:
        assert True
