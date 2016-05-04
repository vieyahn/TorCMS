# -*- coding:utf-8 -*-

import config
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.whoosh_tool import yunsearch
from torcms.core import tools
from torcms.model.mcatalog import MCatalog
from torcms.model.mpost import MPost
from torcms.model.mpost2catalog import MPost2Catalog


class SearchHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mpost2catalog = MPost2Catalog()
        self.ysearch = yunsearch()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == '':
            return
        elif len(url_arr) == 1:
            self.search(url_str)
        elif len(url_arr) == 2:
            self.search(url_arr[0], int(url_arr[1]))
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=  self.userinfo)

    def post(self, url_str=''):
        keyword = self.get_argument('keyword')
        self.search(keyword)

    def search(self, keyword, p_index=1):
        res_all = self.ysearch.get_all_num(keyword)
        results = self.ysearch.search_pager(keyword, page_index=p_index, doc_per_page=20)
        page_num = int(res_all / 20)
        kwd = {'title': '查找结果',
               'pager': '',
               }
        self.render('{0}/search/search.html'.format(self.tmpl_name),
                    kwd=kwd,
                    srecs=results,
                    pager=tools.gen_pager_bootstrap_url('/search/{0}'.format(keyword), page_num, p_index),
                    userinfo = self.userinfo,
                    cfg = config.cfg,
                    )
