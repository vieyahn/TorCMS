# -*- coding:utf-8 -*-

import json
import random
import tornado.escape
import tornado.web

import config
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.app2label_model import MApp2Label
from torcms.model.app_model import MApp
from torcms.model.app_rel_model import MAppRel
from torcms.model.app_reply_model import MApp2Reply
from torcms.model.evaluation_model import MEvaluation
from torcms.model.mappcatalog import MAppCatalog
from torcms.model.usage_model import MUsage
from torcms.model.app2catalog_model import MApp2Catalog


class InfoHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.mevaluation = MEvaluation()
        self.mapp2catalog = MApp2Catalog()
        self.mapp2tag = MApp2Label()
        self.minfo = MApp()
        self.musage = MUsage()
        self.mcat = MAppCatalog()
        self.mrel = MAppRel()
        self.mreply = MApp2Reply()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1 and len(url_str) == 4:
            self.view_info(url_str)

        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1])
            else:
                self.redirect('/user/login')
        elif url_arr[0] == 'comment_add':
            self.add_comment(url_arr[1])

        else:
            return False

    @tornado.web.authenticated
    def add_comment(self, id_post):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_id'] = self.userinfo.uid
        post_data['user_name'] = self.userinfo.user_name
        comment_uid = self.mreply.insert_data(post_data, id_post)
        if comment_uid:
            output = {
                'pinglun': comment_uid,
            }
        else:
            output = {
                'pinglun': 0,
            }
        return json.dump(output, self)

    def gen_daohang_html(self, cat_id):
        '''
        面包屑导航, 可以做成模块
        '''
        return ''
        # parent_id = cat_id[:2] + '00'
        # parent_catname = self.mcat.get_by_id(parent_id).name
        # print('=-' * 20)
        # print(cat_id)
        # catname = self.mcat.get_by_id(cat_id).name
        #
        # daohang_str = '<a href="/">数据中心</a>'
        # daohang_str += ' &gt; <a href="/list/{0}">{1}</a>'.format(parent_id, parent_catname)
        # daohang_str += ' &gt; <a href="/list/{0}">{1}</a>'.format(cat_id, catname)
        # return (daohang_str)

    def view_info(self, app_id):
        qian = self.get_secure_cookie('map_hist')

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        if qian:
            qian = qian.decode('utf-8')
        else:
            qian = ''
        self.set_secure_cookie('map_hist', (app_id + qian)[:20])
        replys = self.mreply.get_by_id(app_id)
        rec = self.minfo.get_by_uid(app_id)
        if 'def_cat_uid' in rec.extinfo and rec.extinfo['def_cat_uid'] != '':
            cat_id = rec.extinfo['def_cat_uid']
        else:
            cat_id = False

        if rec == False:
            kwd = {
                'info': '您要找的云算应用不存在。',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )
            return False

        last_map_id = self.get_secure_cookie('use_app_uid')

        if last_map_id:
            last_map_id = last_map_id.decode('utf-8')

        self.set_secure_cookie('use_app_uid', app_id)

        if last_map_id and self.minfo.get_by_uid(last_map_id):
            self.add_relation(last_map_id, app_id)

        cookie_str = tools.get_uuid()
        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': cookie_str,
            'marker': 1 if 'marker' in post_data  else 0,
            'geojson': post_data['gson'][0] if 'gson' in post_data else '',
            'signature': app_id,
            'tdesc': '',
            'eval_0': self.mevaluation.app_evaluation_count(app_id, 0),
            'eval_1': self.mevaluation.app_evaluation_count(app_id, 1),
            'site_url': config.site_url,
            'login': 1 if self.get_current_user() else 0,

            'daohangstr': self.gen_daohang_html(cat_id),

            'has_image': 0,
            'parentlist': self.mcat.get_parent_list(),

        }

        self.minfo.view_count_increase(app_id)

        if self.get_current_user():
            self.musage.add_or_update(self.userinfo.uid, app_id)

        self.set_cookie('user_pass', cookie_str)

        map_hist = []
        if self.get_secure_cookie('map_hist'):
            for xx in range(0, len(self.get_secure_cookie('map_hist').decode('utf-8')), 4):
                map_hist.append(self.get_secure_cookie('map_hist').decode('utf-8')[xx: xx + 4])

        rel_recs = self.mrel.get_app_relations(rec.uid, 4)

        rand_recs = self.minfo.query_random(4 - rel_recs.count() + 2)

        if cat_id:
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'tmpl_applite/app/show_map.html'
        self.render(tmpl,
                    kwd=kwd,
                    calc_info=rec,
                    userinfo=self.userinfo,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    unescape=tornado.escape.xhtml_unescape,
                    ad_switch=random.randint(1, 18),
                    tag_info=self.mapp2tag.get_by_id(app_id),
                    recent_apps=self.musage.query_recent(self.get_current_user(), 6)[1:],
                    map_hist=map_hist,
                    post_info=rec,
                    replys=replys,
                    )

    def add_relation(self, f_uid, t_uid):
        if False == self.minfo.get_by_uid(t_uid):
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True
