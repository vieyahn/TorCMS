# -*- coding:utf-8 -*-

import json
import random

import tornado.escape
import tornado.web
from torcms.model.app2label_model import MApp2Label
from torcms.model.app_model import MApp
from torcms.model.app_rel_model import MAppRel
from torcms.model.app_reply_model import MApp2Reply
from torcms.model.evaluation_model import MEvaluation
from torcms.model.mappcatalog import MAppCatalog
from torcms.model.usage_model import MUsage

import config
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.app2catalog_model import MApp2Catalog


class MetaHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mevaluation = MEvaluation()
        self.mapp2catalog = MApp2Catalog()
        self.mapp2tag = MApp2Label()
        self.mapp = MApp()
        self.musage = MUsage()
        self.mtag = MAppCatalog()
        self.mrel = MAppRel()
        self.mreply = MApp2Reply()

    def get(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'cat_add':
            self.user_to_add(url_arr[1])
        elif url_arr[0] == 'catalog':
            self.catalog()
        elif len(url_arr) == 1 and len(url_str) == 4:
            self.redirect('/info/{0}'.format(url_arr[0]))
        elif len(url_arr) == 2:
            if url_arr[0] == 'edit':
                self.to_edit_app(url_arr[1])
            elif url_arr[0] == 'add':
                self.to_add_app(url_arr[1])
            else:
                '''
                从相关计算中过来的。
                '''
                self.mrel.update_relation(url_arr[1], url_arr[0])
                self.redirect('/{0}/{1}'.format(config.app_url_name, url_arr[0]))
        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'to_add':
            self.add()
        elif url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1])
            else:
                self.redirect('/user/login')
        elif url_arr[0] == 'comment_add':
            self.add_comment(url_arr[1])
        elif url_arr[0] == 'edit':
            self.update(url_arr[1])
        elif url_arr[0] == 'add':
            self.add(url_arr[1])
        else:
            return False

    def catalog(self):
        self.render('tmpl_applite/app/catalog.html',
                    userinfo=self.userinfo,
                    kwd={'uid': '',}
                    )

    @tornado.web.authenticated
    def user_to_add(self, catid):
        if self.is_admin():
            pass
        else:
            return

        uid = tools.get_uu4d()
        while self.mapp.get_by_uid(uid):
            uid = tools.get_uu4d()
        kwd = {
            'uid': uid,
            'userid': self.userinfo.user_name,
            'def_cat_uid': catid,
            'parentname': self.mtag.get_by_id(catid[:2] + '00').name,
            'catname': self.mtag.get_by_id(catid).name,
        }
        self.render('autogen/add/add_{0}.html'.format(catid), kwd=kwd)

    @tornado.web.authenticated
    def to_add_app(self, uid):
        if self.mapp.get_by_uid(uid):
            self.redirect('/map/edit/{0}'.format(uid))
        else:
            self.render('tmpl_applite/app/add.html',
                        tag_infos=self.mtag.query_all(),
                        userinfo=self.userinfo,
                        kwd={'uid': uid,}
                        )

    @tornado.web.authenticated
    def to_edit_app(self, infoid):
        if self.is_admin():
            pass
        else:
            return False

        rec_info = self.mapp.get_by_uid(infoid)

        if rec_info:
            pass
        else:
            self.render('html/404.html')
            return
        if 'def_cat_uid' in rec_info.extinfo :
            catid = rec_info.extinfo['def_cat_uid']
        else:
            catid = ''

        kwd = {
            'def_cat_uid': catid,
            'parentname': self.mtag.get_by_id(catid[:2] + '00').name if catid != '' else '',
            'catname': self.mtag.get_by_id(catid).name if catid != '' else '',
            'parentlist': self.mtag.get_parent_list(),
            'userip': self.request.remote_ip

        }

        if catid:
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'tmpl_applite/app/edit.html'

        self.render(tmpl,
                    kwd=kwd,
                    calc_info = rec_info,
                    post_info=rec_info,
                    userinfo=self.userinfo,
                    app_info=rec_info,
                    unescape=tornado.escape.xhtml_unescape,
                    tag_infos=[],
                    app2label_info=self.mapp2tag.get_by_id(infoid), )

    # @tornado.web.authenticated
    # def to_edit_app(self, app_id):
    #     if self.userinfo.privilege[4] == '1':
    #         info = self.mapp.get_by_uid(app_id)
    #         self.render('tmpl_applite/app/edit.html',
    #                     userinfo = self.userinfo,
    #                     app_info=info,
    #                     unescape=tornado.escape.xhtml_escape,
    #                     tag_infos=self.mtag.query_all(),
    #                     app2tag_info=self.mapp2catalog.query_by_app_uid(app_id),
    #                     app2label_info=self.mapp2tag.get_by_id(app_id),
    #                     )
    #     else:
    #         return False

    @tornado.web.authenticated
    def update(self, uid):
        if self.is_admin():
            pass
        else:
            return

        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)

        ext_dic['def_uid'] = str(uid)
        if 'def_cat_uid' in post_data:
            ext_dic['def_cat_uid'] = post_data['def_cat_uid'][0]

        ext_dic = self.extra_data(ext_dic, post_data)
        self.mapp.modify_meta(uid,
                              post_data,
                              extinfo=ext_dic)
        self.update_catalog(uid)
        self.update_tag(uid)
        self.redirect('/info/{0}'.format(uid))

    @tornado.web.authenticated
    def add(self, uid=''):
        if self.userinfo.privilege[4] == '1':
            pass
        else:
            return False
        ext_dic = {}
        post_data = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)

        if uid == '':
            uid = tools.get_uu4d()
            while self.mapp.get_by_uid(uid):
                uid = tools.get_uu4d()
            post_data['uid'][0] = uid

        ext_dic['def_uid'] = str(uid)
        ext_dic['def_cat_uid'] = post_data['def_cat_uid'][0]

        ext_dic = self.extra_data(ext_dic, post_data)
        self.mapp.modify_meta( ext_dic['def_uid'],
                              post_data,
                              extinfo=ext_dic)
        self.update_catalog(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/list/{0}'.format(ext_dic['def_cat_uid']))

    @tornado.web.authenticated
    def extra_data(self, ext_dic, post_data):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return ext_dic

    @tornado.web.authenticated
    def update_tag(self, signature):
        if self.userinfo.privilege[4] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        current_tag_infos = self.mapp2tag.get_by_id(signature)

        tags_arr = [x.strip() for x in post_data['tags'][0].split(',')]
        for tag_name in tags_arr:
            if tag_name == '':
                pass
            else:
                self.mapp2tag.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            if cur_info.tag.name in tags_arr:
                pass
            else:
                self.mapp2tag.remove_relation(signature, cur_info.tag)

    @tornado.web.authenticated
    def update_catalog(self, signature):
        if self.userinfo.privilege[4] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        current_catalog_infos = self.mapp2catalog.query_by_app_uid(signature)

        new_tag_arr = []
        for key in ['cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5']:
            if key in post_data:
                if post_data[key][0] == '':
                    pass
                else:
                    new_tag_arr.append(post_data[key][0])
                    self.mapp2catalog.add_record(signature, post_data[key][0], int(key[-1]))
            else:
                pass
        for cur_info in current_catalog_infos:
            if str(cur_info.catalog.uid).strip() in new_tag_arr:
                pass
            else:
                self.mapp2catalog.remove_relation(signature, cur_info.catalog)

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



    def add_relation(self, f_uid, t_uid):
        if False == self.mapp.get_by_uid(t_uid):
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True
