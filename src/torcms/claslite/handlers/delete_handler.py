# -*- coding:utf-8 -*-

import tornado.web

from torcms.claslite.model.catalog_model import MCatalog
from torcms.claslite.model.infor_model import MInfor
from torcms.core.base_handler import BaseHandler


class DeleteHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.minfo = MInfor()
        self.mcat = MCatalog()
        self.template_dir_name = 'tmpl_claslite'

    def get(self, input=''):
        if len(input) == 36:
            inf = self.minfo.get_by_id(input)
            if inf is None:
                self.render('html/404.html')
                return
            self.delete(input)
        else:
            self.render('html/404.html')

    @tornado.web.authenticated
    def delete(self, infoid):
        if self.is_admin():
            pass
        else:
            return False

        post_data = self.minfo.get_by_id(infoid)
        if self.minfo.delete_by_uid(infoid):
            self.redirect('/list/{0}'.format(post_data['catid'][0]))
        else:
            return False

