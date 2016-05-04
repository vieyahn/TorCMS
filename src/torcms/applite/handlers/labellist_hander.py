# -*- coding:utf-8 -*-
import tornado.escape

import config
from torcms.applite.model.app2label_model import MAppLabel, MApp2Label
from torcms.applite.model.app_model import MApp
from torcms.core.base_handler import BaseHandler


class AppLabellistHandler(BaseHandler):
    def initialize(self):
        self.init()

        self.mequa = MApp()
        self.mtag = MAppLabel()
        self.mapp2tag = MApp2Label()



    def get(self, url_str=''):
        if url_str == '':
            self.list(all)

        if len(url_str) > 0:
            url_arr = url_str.split(r'/')

        if len(url_arr) == 1:
            self.list(url_str)
        elif len(url_arr) == 2:
            self.list(url_arr[0], url_arr[1])

    def post(self, url_str=''):
        if len(url_str) > 0:
            url_arr = url_str.split('/')
        if url_arr[0] == 'edit':
            self.edit(url_arr[1])

    def list(self, tag_slug, cur_p=''):
        '''
        根据 cat_handler.py 中的 def view_cat_new(self, cat_slug, cur_p = '')
        :param tag_slug:
        :return:
        '''
        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)

        num_of_tag = self.mtag.catalog_record_number()
        page_num = int(num_of_tag / config.page_num ) + 1


        tag_info = self.mtag.get_all()
        for ii in tag_info:
            tag_count = self.mapp2tag.query_count(ii.uid)
            self.mtag.update_count(ii.uid,tag_count)

        tag_name = 'fd'
        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,
            'title': tag_name,

        }

        self.render('tmpl_applite/label_list/list.html',
                    tag_infos=self.mtag.get_all_by_count(current_page_number),
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    pager=self.gen_pager(tag_slug, page_num, current_page_number),
                    userinfo=self.userinfo,

                    )

    def gen_pager(self, cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面
        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class="{0}">
        <a href="/map/label_list/all">首页</a>
                    </li>'''.format('hidden' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class="{0}">
                    <a href="/map/label_list/all/{2}">&lt; 前页</a>
                    </li>
                    '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class="{0}">
                    <a href="/map/label_list/all/{2}">{2}</a></li>
                    '''.format('active' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class="{0}">
                    <a href="/map/label_list/all/{2}">后页 &gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class="{0}">
                    <a href="/map/label_list/all/{2}">末页</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)
