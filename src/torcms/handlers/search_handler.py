# -*- coding:utf-8 -*-

import config
from torcms.core.base_handler import BaseHandler
# from torcms.core.tool.whoosh_tool import yunsearch
from torcms.core.tool.whoosh_tool import yunsearch

from torcms.core import tools
from torcms.model.minforcatalog import MInforCatalog
from torcms.model.mpost import MPost


class SearchHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MInforCatalog()
        # self.cats = self.mcat.query_all()
        # self.mpost2catalog = MPost2Catalog()
        self.ysearch = yunsearch()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == '':
            return
        elif len(url_arr) == 2:
            self.search(url_arr[0], int(url_arr[1]))
        elif len(url_arr) == 3:
            self.search_cat(url_arr[0], url_arr[1], int(url_arr[2]))
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

    def post(self, url_str=''):
        catid = self.get_argument('searchcat')
        keyword = self.get_argument('keyword')
        if catid == '':
            self.redirect('/search/{0}/1'.format(keyword))
        else:
            self.redirect('/search/{0}/{1}/1'.format(catid, keyword))


    def search(self, keyword, p_index=1):
        res_all = self.ysearch.get_all_num(keyword)
        results = self.ysearch.search_pager(keyword, page_index=p_index, doc_per_page=20)
        page_num = int(res_all / 20)
        kwd = {'title': '查找结果',
               'pager': '',
               'count': res_all,
               'keyword': keyword,
               }
        self.render('doc/search/search.html',
                    kwd=kwd,
                    srecs=results,
                    pager=tools.gen_pager_bootstrap_url('/search/{0}'.format(keyword), page_num, p_index),
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )


    def search_cat(self, catid,  keyword, p_index=1):
        res_all = self.ysearch.get_all_num(keyword, catid=catid)
        results = self.ysearch.search_pager(keyword, catid= catid, page_index=p_index, doc_per_page=20)
        page_num = int(res_all / 20)
        kwd = {'title': '查找结果',
               'pager': '',
               'count': res_all,
               'keyword': keyword,
               'catname': '文档' if catid == '0000' else self.mcat.get_by_uid(catid).name,
               }
        self.render('doc/search/search.html',
                    kwd=kwd,
                    srecs=results,
                    pager=tools.gen_pager_bootstrap_url('/search/{0}/{1}'.format(catid, keyword), page_num, p_index),
                    userinfo=self.userinfo,
                    cfg=config.cfg,

                    )