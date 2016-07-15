# -*- coding:utf-8 -*-

import config
from torcms.core.base_handler import BaseHandler
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
                    pager=self.gen_pager_bootstrap_url('/search/{0}'.format(keyword), page_num, p_index),
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    def gen_pager_bootstrap_url(self,cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面

        if page_num == 1 or page_num == 0:
            pager = ''


        elif page_num > 1:
                pager_mid = ''
                pager_pre = ''
                pager_next = ''
                pager_last = ''
                pager_home = ''

                pager = '<ul class="pagination">'

                if current > 1:
                    pager_home = '''

                      <li class="{0}" name='fenye' onclick='change(this);'
                      ><a href="{1}/{2}">首页</a></li>'''.format( '', cat_slug,1)

                    pager_pre = ''' <li class="{0}" name='fenye' onclick='change(this);'>
                    <a href="{1}/{2}">上一页</a></li>'''.format(  '',  cat_slug, current - 1)
                if current > 5:
                    cur_num = current - 4
                else:
                    cur_num = 1

                if page_num > 10 and cur_num < page_num - 10:
                    show_num = cur_num + 10

                else:
                    show_num = page_num + 1

                for num in range(cur_num,show_num):
                    if num == current:
                        checkstr = 'active'
                    else:
                        checkstr = ''

                    tmp_str_df = '''

                      <li class="{0}" name='fenye' onclick='change(this);'>
                      <a href="{1}/{2}">{2}</a></li>'''.format( checkstr, cat_slug, num)

                    pager_mid += tmp_str_df
                if current < page_num:
                    pager_next = '''

                      <li class="{0}" name='fenye' onclick='change(this);'
                      ><a href="{1}/{2}">下一页</a></li>'''.format( '',  cat_slug, current + 1)
                    pager_last = '''

                      <li class="{0}" name='fenye' onclick='change(this);'
                     ><a href="{1}/{2}">末页</a></li>'''.format(  '', cat_slug, page_num)


                pager += pager_home + pager_pre + pager_mid + pager_next + pager_last
                pager += '</ul>'
        else:
            pass

        return (pager)

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
                    pager=self.gen_pager_bootstrap_url('/search/{0}/{1}'.format(catid, keyword), page_num, p_index),
                    userinfo=self.userinfo,
                    cfg=config.cfg,

                    )