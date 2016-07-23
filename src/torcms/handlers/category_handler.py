# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web
import config

from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.mcatalog import MCatalog
from torcms.model.mpost import MPost
from torcms.model.mpost2catalog import MPost2Catalog


class CategoryHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mpost2catalog = MPost2Catalog()


    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.list_catalog(url_str)
        elif len(url_arr) == 2:
            self.list_catalog(url_arr[0], url_arr[1])
        else:
            self.render('html/404.html')

    def list_catalog(self, cat_slug, cur_p=''):
        if cur_p == '':
            current_page_num = 1
        else:
            current_page_num = int(cur_p)

        current_page_num = 1 if current_page_num < 1 else current_page_num
        cat_rec = self.mcat.get_by_slug(cat_slug)
        num_of_cat = self.mpost2catalog.count_of_certain_catalog(cat_rec.uid)
        page_num = int(num_of_cat / config.page_num) + 1
        cat_name = cat_rec.name
        kwd = {
            'cat_name': cat_name,
            'cat_slug': cat_slug,
            'unescape': tornado.escape.xhtml_unescape,
            'title': cat_name,
            'current_page': current_page_num
        }

        self.render('doc/catalog/list.html',
                    infos=self.mpost2catalog.query_pager_by_slug(cat_slug, current_page_num),
                    pager=tools.gen_pager_purecss('/category/{0}'.format(cat_slug), page_num, current_page_num),
                    userinfo=self.userinfo,
                    unescape = tornado.escape.xhtml_unescape,
                    cfg = config.cfg,
                    kwd=kwd)

    # def get_random(self):
    #     return self.mpost.query_random()
