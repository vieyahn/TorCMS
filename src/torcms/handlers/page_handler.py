# -*- coding:utf-8 -*-
import json

import tornado.escape
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.mcatalog import MCatalog
from torcms.model.mpage import MPage


class PageHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpage = MPage()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'modify':
            self.to_modify(url_arr[1])
        elif url_str == 'list':
           self.list()
        elif url_arr[0] == 'ajax_count_plus':
            self.ajax_count_plus(url_arr[1])
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            self.wiki(url_str.split('.')[0])
        else:
            self.render('html/404.html', userinfo = self.userinfo, kwd = {})

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        else:
            self.wikinsert()

    def wiki(self, slug):
        dbdate = self.mpage.get_by_slug(slug)
        if dbdate:
            self.viewit(dbdate)
        else:
            self.to_add(slug)

    @tornado.web.authenticated
    def to_add(self, citiao):
        kwd = {
            'cats': self.cats,
            'slug': citiao,
            'pager': '',
        }
        self.render('{0}/page/page_add.html'.format(self.tmpl_name),
                    kwd=kwd,
                    userinfo = self.userinfo,)

    @tornado.web.authenticated
    def update(self, slug):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        if 'slug' in post_data:
            pass
        else:
            self.set_status(400)
            return False

        self.mpage.update(slug, post_data)
        self.redirect('/page/{0}.html'.format(post_data['slug'][0]))

    @tornado.web.authenticated
    def to_modify(self, slug):
        kwd = {
            'pager': '',

        }
        self.render('{0}/page/page_edit.html'.format(self.tmpl_name),
                    view=self.mpage.get_by_slug(slug),
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    cfg  = config.cfg,
                    userinfo = self.userinfo,
                    )

    def viewit(self, dbdata):
        kwd = {
            'pager': '',
            'editable': 1 if self.get_current_user() else 0,
        }
        self.render('{0}/page/page_view.html'.format(self.tmpl_name),
                    view=dbdata,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg = config.cfg
                    )

    def ajax_count_plus(self, slug):
        output = {
            'status': 1 if self.mpage.view_count_plus(slug) else 0,
        }

        return json.dump(output, self)

    def list(self):
        kwd = {
                    'pager': '',
                    'unescape': tornado.escape.xhtml_unescape,
                    'title': '单页列表',
                }
        self.render('{0}/{1}/page_list.html'.format(self.tmpl_name, self.tmpl_router),
                    kwd=kwd,
                    view=self.mpage.query_recent(),
                    view_all=self.mpage.query_all(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=config.cfg
                    )

    @tornado.web.authenticated
    def wikinsert(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        if 'slug' in post_data:
            pass
        else:
            self.set_status(400)
            return False

        if self.mpage.get_by_slug(post_data['slug'][0]) is None:
            self.mpage.insert_data(post_data)
        else:
            self.set_status(400)
            return False

        self.redirect('/page/{0}.html'.format(post_data['slug'][0]))

class PageAjaxHandler(PageHandler):
    def initialize(self):
        self.init()
        self.mpage = MPage()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.tmpl_router = 'page_ajax'
