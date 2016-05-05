# -*- coding:utf-8 -*-

from torcms.applite.model.app_model import MApp

from torcms.core.base_handler import BaseHandler
from torcms.model.usage_model import MUsage


class ListHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mequa = MApp()
        self.musage = MUsage()


    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)


        if url_str == 'app':
            self.list_app()

    def list_app(self):
        kwd = {
            'pager': '',
            'title': '最近使用的运算应用' ,
        }
        self.render('tmpl_applite/calc/list_app.html', kwd=kwd,
                    userinfo  = self.userinfo,)
