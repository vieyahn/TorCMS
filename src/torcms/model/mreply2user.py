# -*- coding:utf-8 -*-

import datetime
import time

import peewee
import tornado.escape
import config
from torcms.core import tools
from torcms.model.core_tab import CabPost2Catalog, CabVoter2Reply, CabReply
from torcms.model.core_tab import CabPost2Reply
from torcms.model.ext_tab import TabApp2Reply
from torcms.model.msingle_table import MSingleTable


class MReply2User(MSingleTable):
    def __init__(self):
        self.tab = CabVoter2Reply
        try:
            CabVoter2Reply.create_table()
        except:
            pass

    def update(self, uid, post_data, update_time=False):
        pass
        # cnt_html = tools.markdown2html(post_data['cnt_md'][0])
        #
        # entry = CabVoter2Reply.update(
        #     title=post_data['title'][0],
        #     date=datetime.datetime.now(),
        #     cnt_html=cnt_html,
        #     user_name=post_data['user_name'],
        #     cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
        #     time_update=time.time(),
        #     logo=post_data['logo'][0],
        #     keywords=post_data['keywords'][0],
        #     src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
        # ).where(CabVoter2Reply.uid == uid)
        #
        # entry.execute()

    def insert_data(self, user_id, reply_id):

        record = CabVoter2Reply.select().where(
            (CabVoter2Reply.reply_id == reply_id) & (CabVoter2Reply.voter_id == user_id))

        if record.count() > 0:
            return (False)

        try:
            CabVoter2Reply.create(
                uid=tools.get_uuid(),
                reply_id=reply_id,
                voter_id=user_id,
                timestamp=time.time(),
            )
            return CabVoter2Reply.select().where(CabVoter2Reply.reply_id == reply_id).count()

        except:
            return False

    def delete(self, del_id):
        try:
            del_count2 = CabVoter2Reply.delete().where(CabVoter2Reply.reply_id == del_id)
            del_count2.execute()

            del_count3 = CabPost2Reply.delete().where(CabPost2Reply.reply_id == del_id)
            del_count3.execute()

            del_count4 = TabApp2Reply.delete().where(TabApp2Reply.reply_id == del_id)
            del_count4.execute()

            del_count = CabReply.delete().where(CabReply.uid == del_id)
            del_count.execute()

            return True
        except:

            return False

    def query_cat_random(self, cat_id, num=6):
        if cat_id == '':
            return self.query_random(num)
        if config.dbtype == 1 or config.dbtype == 3:
            return CabVoter2Reply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
                peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabVoter2Reply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
                peewee.fn.Rand()).limit(num)

    def get_num_by_cat(self, cat_str):
        return CabVoter2Reply.select().where(CabVoter2Reply.id_cats.contains(',{0},'.format(cat_str))).count()

    def query_keywords_empty(self):
        return CabVoter2Reply.select().where(CabVoter2Reply.keywords == '')

    def query_dated(self, num=8):
        return CabVoter2Reply.select().order_by(CabVoter2Reply.time_update).limit(num)

    def query_cat_recent(self, cat_id, num=8):
        return CabVoter2Reply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
            CabVoter2Reply.time_update.desc()).limit(num)

    def query_most(self, num=8):
        return CabVoter2Reply.select().order_by(CabVoter2Reply.view_count.desc()).limit(num)

    def update_view_count(self, citiao):
        entry = CabVoter2Reply.update(view_count=CabVoter2Reply.view_count + 1).where(CabVoter2Reply.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = CabVoter2Reply.update(view_count=CabVoter2Reply.view_count + 1).where(CabVoter2Reply.uid == uid)
        entry.execute()

    def update_keywords(self, uid, inkeywords):
        entry = CabVoter2Reply.update(keywords=inkeywords).where(CabVoter2Reply.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        tt = CabVoter2Reply.select().where(CabVoter2Reply.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return CabVoter2Reply.get(CabVoter2Reply.title == citiao)

    def get_next_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabVoter2Reply.select().where(CabVoter2Reply.time_update < current_rec.time_update).order_by(
            CabVoter2Reply.time_update.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()

    def get_previous_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabVoter2Reply.select().where(CabVoter2Reply.time_update > current_rec.time_update).order_by(
            CabVoter2Reply.time_update)
        if query.count() == 0:
            return None
        else:
            return query.get()
