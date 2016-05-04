# -*- coding:utf-8 -*-

import time

import tornado.web

from torcms.core import tools
from torcms.claslite.model.catalog_model import MCatalog
from torcms.core.base_handler import BaseHandler
from torcms.claslite.model.infor_model import MInfor


class AddHandler( BaseHandler ):
    def initialize(self, hinfo=''):
        self.init()
        self.minfo = MInfor()
        self.mcat = MCatalog()
        self.template_dir_name = 'tmpl_claslite'


    def get(self, url_str=''):
        if len(url_str) == 4:
            self.to_add(url_str)
        else:
            self.render('html/404.html', kwd = {'info': '非法输入，请选择正确的类别!'})

    def post(self, url_str=''):
        if len(url_str) == 4:
            self.add()
        else:
            self.render('html/404.html', kwd = {'info': '非法输入，请选择正确的类别!'})


    @tornado.web.authenticated
    def to_add(self, catid, vip='0'):
        if self.userinfo.privilege[4] == '1':
            pass
        else:
            return

        ip = self.request.remote_ip
        uid = tools.get_uu4d()
        while self.minfo.get_by_id(uid):
            uid = tools.get_uu6d()
        kwd = {
            'uid': uid,
            'userid': self.userinfo.user_name,
            'catid': catid,
            'parentid': catid[:2] + '00',
            'parentname': self.mcat.get_by_id(catid[:2] + '00').name,
            'catname': self.mcat.get_by_id(catid).name,
            'userip': ip,
            'vip': vip,
        }
        self.render('autogen/add/add_{1}.html'.format(self.template_dir_name, catid), kwd=kwd)

    @tornado.web.authenticated
    def add(self):
        if self.userinfo.privilege[2] == '1':
            pass
        else:
            return

        post_data = { }
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        uid = post_data['uid'][0][:4]
        # 对uid进行判断，防止反复发布同一信息。
        uu = self.minfo.get_by_id(uid)
        if uu:
            self.render('not_repeat.html')
            return False

        ts = tools.timestamp()

        post_data['catname'] = self.mcat.get_by_id(post_data['catid'][0]).name
        post_data['userid'] = self.userinfo.user_name
        # post_data['views'] = 1
        # post_data['create_time'] = ts
        # post_data['update_time'] = ts

        # 添加控制字段
        post_data['def_uid'] = str(uid)
        post_data['def_create_time_str'] = time.localtime(ts)
        post_data['def_update_time_str'] = time.localtime(ts)

        # 记录的超时的时间
        # 推广
        post_data['def_tuiguang_out_time'] = ts
        # 置顶
        post_data['def_zhiding'] = 0
        post_data['def_zhiding_out_time'] = ts
        # 刷新
        post_data['def_refresh'] = 1
        # post_data['def_refresh_out_time'] = ts + c.refresh_timeout
        # 是否有效。是否通过审核
        post_data['def_valid'] = 1
        post_data['def_banned'] = 0
        post_data['keywords'] = [x.strip() for x in post_data['keywords'][0].split(',')]
        post_data['def_tuiguang'] = 0

        if self.minfo.insert_data(self.userinfo.uid, post_data):
            self.redirect('/list/{0}'.format(post_data['catid'][0]))
        else:
            self.render('{0}/html/error.html'.format(self.template_dir_name))
