# -*- coding:utf-8 -*-

import tornado.web

from torcms.claslite.model.catalog_model import MCatalog


class ImgSlide(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('tmpl_claslite/modules/img_slide.html', post_info=info)


class UserInfo(tornado.web.UIModule):
    def render(self, uinfo, uop):
        return self.render_string('tmpl_claslite/modules/user_info.html', userinfo=uinfo, userop=uop)


class VipInfo(tornado.web.UIModule):
    def render(self, uinfo, uvip):
        return self.render_string('tmpl_claslite/modules/vip_info.html', userinfo=uinfo, uservip=uvip)


class ToplineModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('tmpl_claslite/modules/topline.html')


class BannerModule(tornado.web.UIModule):
    def __init__(self, parentid=''):
        self.parentid = parentid

    def render(self):
        self.mcat = MCatalog()
        parentlist = self.mcat.get_parent_list()
        kwd = {
            'parentlist': parentlist,
            'parentid': self.parentid,
        }
        return self.render_string('tmpl_claslite/modules/banner.html', kwd=kwd)


class BreadCrumb(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('tmpl_claslite/modules/bread_crumb.html', info=info)


class ContactInfo(tornado.web.UIModule):
    def render(self, info):
        # ip_addr = info.extinfo['userip'][0]
        # ip_arr = ip_addr.split('.')
        # if len(ip_arr) > 3:
        #     ip_arr[3] = '*'
        # maskip = '.'.join(ip_arr)
        kwd = {
            'maskip': '',  # maskip,
        }
        return self.render_string('tmpl_claslite/modules/contact_info.html', post_info=info, kwd=kwd)


class BreadcrumbPublish(tornado.web.UIModule):
    def render(self, sig=0):
        kwd = {
            'sig': sig,
        }
        return self.render_string('tmpl_claslite/modules/breadcrumb_publish.html', kwd=kwd)


class InfoList:
    def renderit(self, info=''):
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'
        if len(info.extinfo['mymps_img']) > 0:
            imgname = info.extinfo['mymps_img'][0]
        if info.extinfo['def_zhiding'] == 1:
            zhiding_str = '<span class="red">（已置顶）</span>'
        if info.extinfo['def_tuiguang'] == 1:
            tuiguang_str = '<span class="red">（已推广）</span>'

        list_type = info.extinfo['catid']

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguan': tuiguang_str,
        }

        return self.render_string('tmpl_claslite/infolist/infolist_{0}.html'.format(list_type),
                                  kwd=kwd,
                                  post_info=info)
