# -*- coding:utf-8 -*-

from torcms.applite.model.ext_tab import TabCatalog
from torcms.torlite.model.mcatalog import MCatalog

class MAppCatalog(MCatalog):
    def __init__(self):
        self.tab = TabCatalog
        try:
            TabCatalog.create_table()
        except:
            pass

