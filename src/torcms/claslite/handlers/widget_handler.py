# -*- coding:utf-8 -*-


from torcms.core.base_handler import BaseHandler
from torcms.claslite.model.catalog_model import MCatalog

class WidgetHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.mcat = MCatalog()

    def get(self, input=''):
        if input == 'loginfo':
            self.loginfo()

    def loginfo(self):
        if self.get_secure_cookie("user"):
            self.render('clalite/widget/loginfo.html',
                        username=self.get_secure_cookie("user"))
        else:
            self.render('clalite/widget/tologinfo.html',
                        )
