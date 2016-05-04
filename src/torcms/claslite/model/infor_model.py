# -*- coding:utf-8 -*-

from datetime import datetime
from torcms.core import tools
from torcms.applite.model.ext_tab import TabApp as TabInfor


# class TabInfor(BaseModel):
#     uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
#     title = peewee.CharField(null=False, default='')
#     user = peewee.ForeignKeyField(CabMember, related_name='json_user_rel')
#     desc = peewee.TextField(null=False, default='')
#     view_count = peewee.IntegerField(null=False, default=0)
#     valid = peewee.IntegerField(null=False, default=0)
#     time_create = peewee.IntegerField(null=False, default=0)
#     time_update = peewee.IntegerField(null=False, default=0)
#     public = peewee.IntegerField(null=False, default=0)
#     infor = BinaryJSONField()


class MInfor(object):
    def __init__(self):
        try:
            TabInfor.create_table()
        except:
            pass

    def get_by_id(self, uid):
        try:
            return TabInfor.get(TabInfor.uid == uid)
        except:
            return False

    def query_recent(self, user_id, num=10):
        return TabInfor.select().where(TabInfor.user == user_id).order_by(TabInfor.order).limit(num)

    def query_by_app(self, app_id, user_id):
        return TabInfor.select().where((TabInfor.app == app_id) & (TabInfor.user == user_id)).order_by(
            TabInfor.time_update.desc())

    def delete_by_uid(self, uid):
        q = TabInfor.delete().where(TabInfor.uid == uid)
        try:
            q.execute()
        except:
            return False

    def add_or_update(self, uid, user_id, app_id, geojson):
        current_count = TabInfor.select().where(TabInfor.uid == uid).count()

        if current_count > 0:
            cur_record = self.get_by_id(uid)
            entry = TabInfor.update(
                json=geojson,
                time_update=tools.timestamp(),
            ).where(TabInfor.uid == cur_record.uid)
            entry.execute()

        else:
            entry = TabInfor.create(
                uid=uid,
                title='',
                app=app_id,
                user=user_id,
                json=geojson,
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
                public=1,
            )

    def get_num_condition(self, con):

        return self.get_list(con).count()

    def insert_data(self, user_id, post_data):
        # 防止插入相同 UID的信息，
        # 需要先进行判断
        if self.get_by_id(post_data['def_uid']):
            return False
        # try:
        print(post_data)
        entry = TabInfor.create(
            uid=post_data['def_uid'],
            user=user_id,
            title = post_data['title'][0],
            cnt_md = post_data['cnt_md'][0],
            # cnt_md = post_data['cnt_md'][0],
            # infor= json.dumps(post_data),
            date=datetime.now(),
            extinfo=post_data,
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
            public=1,
        )
        return True
        # except:
        #     return False

    def update(self, uid, post_data):
        entry = TabInfor.update(
            infor=post_data).where(TabInfor.uid == uid)
        entry.execute()
        return True

    def query_by_tagname(self, tag_name):

        # condition = {'keywords': {'$elemMatch': {'$eq': tag_name}}}
        condition = {'keywords': [tag_name]}

        return TabInfor.select().where(TabInfor.extinfo.contains(condition))
        # return TabInfor.select()

    def get_cat_recs_count(self, catid):
        '''
        获取某一分类下的数目
        '''
        condition = {'catid': [catid]}

        db_data = TabInfor.select().where(TabInfor.extinfo.contains(condition))
        return db_data.count()

    def get_list(self, condition):

        db_data = TabInfor.select().where(TabInfor.extinfo.contains(condition))

        return (db_data)

    def get_label_fenye(self, tag_slug, page_num):
        all_list = self.query_by_tagname(tag_slug)

        # 当前分页的记录
        # current_list = all_list[(page_num - 1) * c.info_list_per_page: (page_num) * c.info_list_per_page]
        return (all_list)

    def get_list_fenye(self, tag_slug, page_num):
        # 所有的记录
        all_list = self.get_list(tag_slug)
        # 当前分页的记录
        # current_list = all_list[(page_num - 1) * c.info_list_per_page: (page_num) * c.info_list_per_page]
        return (all_list)
