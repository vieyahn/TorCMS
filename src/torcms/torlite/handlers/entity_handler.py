# -*- coding:utf-8 -*-
import os
import uuid

import tornado.ioloop
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.torlite.model.entry_model import MEntry


class EntityHandler( BaseHandler ):
    def initialize(self):
        self.init()
        self.mpic = MEntry()
        self.tmpl_name= config.torlite_template_name

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == 'add':
            self.to_add()
        elif (url_str == 'list' or url_str == ''):
            self.list()
        elif len(url_str) > 36:
            self.view(url_str)
        else:
            self.render('html/404.html', kwd = {}, userinfo = self.userinfo)

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_str == 'add' or url_str == '':
            self.add_pic()
        else:
            self.render('html/404.html',kwd = {}, userinfo = self.userinfo)

    @tornado.web.authenticated
    def list(self):
        recs = self.mpic.getall()
        kwd = {
            'pager': '',
        }
        self.render('{0}/entry/entry_list.html'.format(self.tmpl_name),
                    imgs=recs,
                    cfg = config.cfg,
                    kwd=kwd,
                    userinfo = self.userinfo)

    @tornado.web.authenticated
    def to_add(self):
        kwd = {
            'pager': '',
        }
        self.render('{0}/entry/entry_add.html'.format(self.tmpl_name),
                    cfg = config.cfg,
                    kwd=kwd,
                    userinfo  = self.userinfo)


    @tornado.web.authenticated
    def add_pic(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]

            (qian, hou) = os.path.splitext(filename)
            signature = str(uuid.uuid1())
            outfilename = '{0}{1}'.format(signature, hou)
            outpath = 'static/upload/{0}'.format(signature[:2])
            if os.path.exists(outpath):
                pass
            else:
                os.mkdir(outpath)
            with open(os.path.join(outpath, outfilename), "wb") as f:
                f.write(file_dict["body"])
            path_save = os.path.join(signature[:2], outfilename)
            self.mpic.insert_data(signature, path_save)
        self.redirect('/entry/{0}'.format(path_save))

    @tornado.web.authenticated
    def view(self, outfilename):
        kwd = {
            'pager': '',

        }
        self.render('{0}/entry/entry_view.html'.format(self.tmpl_name),
                    filename=outfilename,
                    cfg = config.cfg,
                    kwd=kwd,
                    userinfo = self.userinfo,)
