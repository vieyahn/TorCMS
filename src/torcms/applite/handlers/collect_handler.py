# -*- coding:utf-8 -*-

import tornado.web

from torcms.applite.model.app_model import MApp
from torcms.applite.model.app_rel_model import MAppRel
from torcms.applite.model.collect_model import MCollect
from torcms.applite.model.usage_model import MUsage
from torcms.core.base_handler import BaseHandler


class CollectHandler(BaseHandler, ):
    def initialize(self):
        self.init()
        self.mequa = MApp()
        self.musage = MUsage()
        self.mrel = MAppRel()
        self.mcollect = MCollect()



    def get(self, url_str=''):
        if len(url_str) > 0:
            url_arr = url_str.split('/')
        else:
            return False
        if url_str == 'list':
            self.list()
        elif len(url_arr) == 1 and len(url_str) == 4 :
            if self.get_current_user():
                self.add_or_update(url_str)
            else:
                self.set_status('403')
                return False

    @tornado.web.authenticated
    def add_or_update(self, app_id):
        self.mcollect.add_or_update(self.userinfo.uid, app_id)

    @tornado.web.authenticated
    def list(self):
        self.render('tmpl_applite/collect/list.html',
                    recs_collect = self.mcollect.query_recent(self.userinfo.uid, 20),
                    userinfo = self.userinfo,
                    )

