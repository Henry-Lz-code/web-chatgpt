# -*- coding: UTF-8 -*-
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.json', '.secrets.json'],
)
