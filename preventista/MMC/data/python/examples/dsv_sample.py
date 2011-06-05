#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from auto_dsv import import_dsv
from files import get_sd_path
from debug import debug

debug(import_dsv("%s:\\python\data\input\clientes.csv" % get_sd_path()))
