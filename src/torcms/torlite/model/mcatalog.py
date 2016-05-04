# -*- coding:utf-8 -*-


import config
from torcms.torlite.model.core_tab import CabCatalog
from torcms.torlite.model.msingle_table import MSingleTable


class MCatalog(MSingleTable):
    def __init__(self):
        self.tab = CabCatalog
        try:
            CabCatalog.create_table()
        except:
            pass

    def query_uid_starts_with(self, qian2):
        return self.tab.select().where(self.tab.uid.startswith(qian2)).order_by(self.tab.uid)

    def query_all(self, by_uid=True, by_count=False, by_order=False):
        if by_uid:
            recs = self.tab.select().order_by(self.tab.uid)
        elif by_count:
            recs = self.tab.select().order_by(self.tab.count.desc())
        elif by_order:
            recs = self.tab.select().order_by(self.tab.order)
        else:
            recs = self.tab.select().order_by(self.tab.name)
        return (recs)

    def query_field_count(self, limit_num):
        return self.tab.select().order_by(self.tab.count.desc()).limit(limit_num)

    def get_by_slug(self, slug):
        return self.tab.get(slug=slug)

    def update_app_catalog_num(self, cat_id, num):
        entry = self.tab.update(
            count=num,
        ).where(self.tab.uid == cat_id)
        entry.execute()

    def update_post_catalog_num(self, cat_id, num):
        entry = self.tab.update(
            count=num,
        ).where(self.tab.uid == cat_id)
        entry.execute()

    def initial_db(self, post_data):
        entry = self.tab.create(
            name=post_data['name'],
            id_cat=post_data['id_cat'],
            slug=post_data['slug'],
            order=post_data['order'],
        )
        return (entry)

    def update(self, uid, post_data, update_time=False):

        if update_time:
            entry = self.tab.update(
                name=post_data['name'][0],
                slug=post_data['slug'][0],
                order=post_data['order'][0],
            ).where(self.tab.uid == uid)
        else:
            entry = self.tab.update(
                name=post_data['name'][0],
                slug=post_data['slug'][0],
                order=post_data['order'][0],
            ).where(self.tab.uid == uid)
        entry.execute()

    def insert_data(self, id_post, post_data):
        uu = self.get_by_id(id_post)
        if uu is None:
            pass
        else:
            return (False)

        entry = self.tab.create(

            name=post_data['name'][0],
            slug=post_data['slug'][0],
            order=post_data['order'][0],
            uid=post_data['uid'][0],
        )
        return (entry.uid)
