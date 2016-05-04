# # -*- coding:utf-8 -*-
#
# from torcms.claslite.model.catalog_model import MCatalog
# from torcms.claslite.model.infor_model import MInfor
# from torcms.core.base_handler import BaseHandler
#
#
# class InfoHandler( BaseHandler ):
#     def initialize(self, hinfo=''):
#         # self.init_condition(config.mongo_collection_name)
#         self.init()
#         self.minfo = MInfor()
#         self.mcat = MCatalog()
#         self.template_dir_name = 'tmpl_claslite'
#
#
#     def get(self, input=''):
#         if len(input) == 4:
#             self.view(input)
#         else:
#             self.render('{0}/404.html'.format(self.template_dir_name))
#
#     def is_viewable(self, info):
#         '''
#         是否可以查看,抽象出来保留备用
#         '''
#         return True
#
#     def gen_daohang_html(self, cat_id):
#         '''
#         面包屑导航, 可以做成模块
#         '''
#         parent_id = cat_id[:2] + '00'
#         parent_catname = self.mcat.get_by_id(parent_id).name
#         catname = self.mcat.get_by_id(cat_id).name
#
#         daohang_str = '<a href="/">数据中心</a>'
#         daohang_str += ' &gt; <a href="/list/{0}">{1}</a>'.format(parent_id, parent_catname)
#         daohang_str += ' &gt; <a href="/list/{0}">{1}</a>'.format(cat_id, catname)
#         return (daohang_str)
#
#     def view(self, uuid):
#         info = self.minfo.get_by_id(uuid)
#
#         if info is None:
#             self.set_status(404)
#             self.render('{0}/404_view.html'.format(self.template_dir_name))
#             return (False)
#         elif self.is_viewable(info):
#             pass
#         else:
#             self.render('{0}/404.html'.format(self.template_dir_name))
#             return
#
#         cat_id = info.extinfo['catid'][0]
#
#         has_image = 0
#         # if len(info.extinfo['mymps_img']) > 0:
#         #     has_image = 1
#
#         kwd = {
#             'daohangstr': self.gen_daohang_html(cat_id),
#             'has_image': has_image,
#             'parentid': cat_id[:2] + '00',
#             'parentlist': self.mcat.get_parent_list(),
#         }
#         # self.update_info_when_view(info)
#         self.render('autogen/view/view_{1}.html'.format(self.template_dir_name, cat_id),
#                     kwd=kwd,
#                     post_info=info)
#
#     def update_info_when_view(self, info):
#         uuid = info['def_uid']
#         self.minfo.update_view_count(uuid)
