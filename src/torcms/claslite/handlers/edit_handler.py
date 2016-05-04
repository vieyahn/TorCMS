# # -*- coding:utf-8 -*-
#
#
# import time
# import tornado.web
# from config import cfg as c
# from torcms.core.base_handler import BaseHandler
# from torcms.claslite.model.catalog_model import MCatalog
# from torcms.claslite.model.infor_model import MInfor
# from torcms.core import tools
#
#
# class EditHandler(BaseHandler):
#     def initialize(self, hinfo=''):
#         self.init()
#         self.minfo = MInfor()
#         self.mcat = MCatalog()
#         self.template_dir_name = 'tmpl_claslite'
#
#     def get(self, input=''):
#         if len(input) == 6:
#             self.toedit(input)
#         else:
#             self.render('html/404.html')
#
#     def post(self, input=''):
#         if len(input) == 6:
#             self.update(input)
#
#
#
#     @tornado.web.authenticated
#     def toedit(self, infoid):
#         if self.is_admin():
#             pass
#         else:
#             return False
#
#         rec_info = self.minfo.get_by_id(infoid)
#
#         if rec_info:
#             pass
#         else:
#             self.render('html/404.html')
#             return
#
#         catid = rec_info.infor['catid'][0]
#
#         kwd = {
#             'catid': catid,
#             'parentid': catid[:2] + '00',
#             'parentname': self.mcat.get_by_id(catid[:2] + '00').catname,
#             'catname': self.mcat.get_by_id(catid).catname,
#             'parentlist': self.mcat.get_parent_list(),
#             'userip': self.request.remote_ip
#
#         }
#         self.render('autogen/edit/edit_{1}.html'.format(self.template_dir_name, catid),
#                     kwd=kwd,
#                     post_info=rec_info)
#
#     @tornado.web.authenticated
#     def update(self, par_uid):
#
#         if self.is_admin():
#             pass
#         else:
#             return False
#         rec_info = self.minfo.get_by_id(par_uid)
#         post_data = rec_info.infor
#
#         for key in self.request.arguments:
#             post_data[key] = self.get_arguments(key)
#
#         ts = tools.timestamp()
#
#         post_data['catname'] = self.mcat.get_by_id(post_data['catid'][0]).catname
#         post_data['userid'] = self.userinfo.user_name
#         post_data['def_uid'] = str(par_uid)
#         post_data['update_time'] = ts
#         post_data['def_update_time_str'] = time.localtime(ts)
#         post_data['def_refresh'] = 1
#         post_data['def_refresh_out_time'] = ts + c.refresh_timeout
#         post_data['def_valid'] = 1
#         post_data['def_banned'] = 0
#         post_data['keywords'] = [x.strip() for x in post_data['keywords'][0].split(',')]
#
#         self.minfo.update(par_uid, post_data)
#
#         self.redirect('/list/{0}'.format(post_data['catid'][0]))
