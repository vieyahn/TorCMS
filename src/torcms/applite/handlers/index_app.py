# -*- coding:utf-8 -*-
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.torlite.model.mcatalog import MCatalog
from torcms.torlite.model.mpost import MPost


class AppIndexHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()


    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html')

    def index(self):
        cstr = tools.get_uuid()
        self.set_cookie('user_pass', cstr)
        kwd = {
            'cookie_str': cstr
        }
        self.render('tmpl_applite/index/index.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    catalog_info=self.mcat.query_all(by_order=True)
                    )
