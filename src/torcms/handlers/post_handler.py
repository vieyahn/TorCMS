# -*- coding:utf-8 -*-

import json

import tornado.escape
import tornado.web
import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.mcatalog import MCatalog
from torcms.model.mlabel_model import MPost2Label
from torcms.model.mpost import MPost
from torcms.model.mpost2catalog import MPost2Catalog
from torcms.model.mpost2reply import MPost2Reply
from torcms.model.mpost_hist import MPostHist
from torcms.model.mrelation import MRelation


class PostHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        self.mpost2reply = MPost2Reply()
        self.mpost2label = MPost2Label()
        self.mrel = MRelation()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.recent()
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            self.wiki(url_str.split('.')[0])
        elif url_str == 'add_document':
            self.to_add_document()
        elif url_str == 'recent':
            self.recent()
        elif url_str == 'refresh':
            self.refresh()
        elif (url_arr[0] == 'modify'):
            self.to_modify(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'ajax_count_plus':
            self.ajax_count_plus(url_arr[1])
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):
        if url_str == '':
            return
        url_arr = url_str.split('/')

        if len(url_arr) == 1 and url_str.endswith('.html'):
            self.add_post()
        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        elif url_str == 'add_document':
            self.user_add_post()
        elif url_arr[0] == 'add_document':
            self.user_add_post()
        else:
            self.redirect('html/404.html')

    def ajax_count_plus(self, uid):
        output = {
            'status': 1 if self.mpost.update_view_count_by_uid(uid) else 0,
        }

        return json.dump(output, self)

    def recent(self, with_catalog=True, with_date=True):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        self.render('doc/post/post_list.html',
                    kwd=kwd,
                    view=self.mpost.query_recent(),
                    view_all=self.mpost.query_all(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    def __could_edit(self, postid):
        post_rec = self.mpost.get_by_uid(postid)
        if not post_rec:
            return False
        if self.check_doc_priv(self.userinfo)['EDIT'] or post_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    def refresh(self):

        kwd = {
            'pager': '',
            'title': '最近文档',
        }
        self.render('doc/post/post_list.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=self.mpost.query_dated(10),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=config.cfg, )

    # def get_random(self):
    #     return self.mpost.query_random()

    def wiki(self, uid):
        if self.mpost.get_by_id(uid):
            self.viewit(uid)
        else:
            self.to_add(uid)

    def to_add_document(self, ):
        if self.check_doc_priv(self.userinfo)['ADD']:
            pass
        else:
            return False
        kwd = {
            'pager': '',
            'cats': self.cats,
            'uid': '',

        }
        self.render('doc/post/post_add.html',
                    kwd=kwd,
                    tag_infos=self.mcat.query_all(),
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    @tornado.web.authenticated
    def to_add(self, uid):
        if self.check_doc_priv(self.userinfo)['ADD']:
            pass
        else:
            return False
        kwd = {
            'cats': self.cats,
            'uid': uid,
            'pager': '',
        }
        self.render('doc/post/post_add.html',
                    kwd=kwd,
                    tag_infos=self.mcat.query_all(),
                    cfg=config.cfg,
                    userinfo=self.userinfo, )

    @tornado.web.authenticated
    def update(self, uid):
        if self.__could_edit(uid):
            pass
        else:
            return False

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_name'] = self.get_current_user()
        is_update_time = True if post_data['is_update_time'][0] == '1' else False
        self.mpost.update(uid, post_data, update_time=is_update_time)
        self.update_catalog(uid)
        self.update_tag(uid)
        self.mpost_hist.insert_data(self.mpost.get_by_id(uid))
        self.redirect('/post/{0}.html'.format(uid))

    @tornado.web.authenticated
    def update_tag(self, signature):
        current_tag_infos = self.mpost2label.get_by_id(signature)
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        if 'tags' in post_data:
            pass
        else:
            return False

        tags_arr = [x.strip() for x in post_data['tags'][0].split(',')]

        for tag_name in tags_arr:
            if tag_name == '':
                pass
            else:
                self.mpost2label.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            if cur_info.tag.name in tags_arr:
                pass
            else:
                self.mpost2label.remove_relation(signature, cur_info.tag)

    @tornado.web.authenticated
    def update_catalog(self, uid):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        current_infos = self.mpost2catalog.query_by_id(uid)
        new_tag_arr = []
        for key in ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']:
            if key in post_data:
                pass
            else:
                continue
            if post_data[key][0] == '':
                pass
            else:
                new_tag_arr.append(post_data[key][0])
                self.mpost2catalog.add_record(uid,
                                              post_data[key][0],
                                              int(key[-1]))

        for cur_info in current_infos:
            if str(cur_info.catalog.uid).strip() not in new_tag_arr:
                self.mpost2catalog.remove_relation(uid, cur_info.catalog)

    @tornado.web.authenticated
    def to_modify(self, id_rec):
        if self.__could_edit(id_rec):
            pass
        else:
            return False

        kwd = {
            'pager': '',
            'cats': self.cats,

        }
        self.render('doc/post/post_edit.html',
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    tag_infos=self.mcat.query_all(),
                    app2label_info=self.mpost2label.get_by_id(id_rec),
                    app2tag_info=self.mpost2catalog.query_by_id(id_rec),
                    dbrec=self.mpost.get_by_id(id_rec),
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    def get_cat_str(self, cats):
        cat_arr = cats.split(',')
        out_str = ''
        for xx in self.cats:
            if str(xx.uid) in cat_arr:
                tmp_str = '''<li><a href="/category/{0}" style="margin:10px auto;"> {1} </a></li>
                '''.format(xx.slug, tornado.escape.xhtml_escape(xx.name))
                out_str += tmp_str

        return (out_str)

    def get_cat_name(self, id_cat):
        for x in self.cats:
            if x['id_cat'] == id_cat:
                return (x['name'])

    def __gen_last_current_relation(self, post_id):
        '''
        Generate the relation for the post and last post viewed.
        :param post_id:
        :return:
        '''
        last_post_id = self.get_secure_cookie('last_post_uid')
        if last_post_id:
            last_post_id = last_post_id.decode('utf-8')
        self.set_secure_cookie('last_post_uid', post_id)

        if last_post_id and self.mpost.get_by_id(last_post_id):
            self.add_relation(last_post_id, post_id)

    def viewit(self, post_id):
        self.__gen_last_current_relation(post_id)

        cats = self.mpost2catalog.query_entry_catalog(post_id)
        replys = self.mpost2reply.get_by_id(post_id)
        tag_info = self.mpost2label.get_by_id(post_id)

        rec = self.mpost.get_by_id(post_id)

        if not rec:
            kwd = {
                'info': '您要查看的页面不存在。',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)
            return False

        if cats.count() == 0:
            cat_id = ''
        else:
            cat_id = cats.get().catalog
        kwd = {
            'pager': '',
            'editable': self.editable(),
            'cat_id': cat_id
        }

        rel_recs = self.mrel.get_app_relations(rec.uid, 4)

        rand_recs = self.mpost.query_random(4 - rel_recs.count() + 2)

        self.render('doc/post/post_view.html',
                    view=rec,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    tag_info=tag_info,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    replys=replys,
                    cfg=config.cfg,
                    )

    def add_relation(self, f_uid, t_uid):
        if self.mpost.get_by_id(t_uid) is False:
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        # 双向关联，但权重不一样.
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True

    @tornado.web.authenticated
    def add_post(self):
        if self.check_doc_priv(self.userinfo)['ADD']:
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.userinfo.user_name
        id_post = post_data['uid'][0]
        cur_post_rec = self.mpost.get_by_id(id_post)
        if cur_post_rec is None:
            uid = self.mpost.insert_data(id_post, post_data)
            self.update_tag(uid)
            self.update_catalog(uid)
        self.redirect('/post/{0}.html'.format(id_post))

    @tornado.web.authenticated
    def user_add_post(self):
        if self.check_doc_priv(self.userinfo)['ADD']:
            pass
        else:
            return False
        post_data = {}

        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        if not ('title' in post_data):
            self.set_status(400)
            return False
        else:
            pass

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uu5d()
        while self.mpost.get_by_id(cur_uid):
            cur_uid = tools.get_uu5d()

        uid = self.mpost.insert_data(cur_uid, post_data)
        self.update_tag(uid)
        self.update_catalog(uid)
        self.redirect('/post/{0}.html'.format(cur_uid))

    @tornado.web.authenticated
    def delete(self, del_id):
        if self.check_doc_priv(self.userinfo)['DELETE']:
            pass
        else:
            return False
        is_deleted = self.mpost.delete(del_id)
        if is_deleted:
            self.redirect('/post/recent')
        else:
            return False


class PostAjaxHandler(PostHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        self.mpost2reply = MPost2Reply()
        self.mpost2label = MPost2Label()
        self.mrel = MRelation()


    @tornado.web.authenticated
    def delete(self, del_id):
        if self.check_doc_priv(self.userinfo)['DELETE']:
            pass
        else:
            return False
        is_deleted = self.mpost.delete(del_id)

        if is_deleted:
            output = {
                'del_info ': 1,
            }
        else:
            output = {
                'del_info ': 0,
            }
        return json.dump(output, self)
