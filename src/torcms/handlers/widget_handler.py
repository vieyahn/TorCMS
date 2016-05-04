# -*- coding:utf-8 -*-

import config
from torcms.core.base_handler import BaseHandler

class WidgetHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()

    def get(self, input=''):
        if input == 'loginfo':
            self.loginfo()

    def loginfo(self):
        if self.get_secure_cookie("user"):
            self.render('tmpl_torlite/widget/loginfo.html',
                        username=self.get_secure_cookie("user"))
        else:
            self.render('tmpl_torlite/widget/tologinfo.html',
                        cfg=config.cfg,
                        userinfo=self.userinfo,

                        )
