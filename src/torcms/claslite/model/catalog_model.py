# -*- coding:utf-8 -*-

import peewee

import config
from torcms.applite.model.ext_tab import TabCatalog as phpmps_category


#
# class phpmps_category(BaseModel):
#     uid = peewee.CharField(max_length=4, null=False, unique=True, help_text='类别的ID', primary_key=True)
#     name = peewee.CharField(max_length=32, null=False, help_text='类别中文名称')
#     pid = peewee.CharField(max_length=4, null=False, )
#     order = peewee.IntegerField()
#     count = peewee.IntegerField()


# uid = peewee.CharField(null=False, max_length=4, index=True, unique=True, primary_key=True, help_text='', )
# slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
# name = peewee.CharField(null=False, max_length=255, help_text='', )
# order = peewee.IntegerField()
# # post_count = peewee.IntegerField(default=0)
# count = peewee.IntegerField(default=0)

class MCatalog():
    def __init__(self):
        self.tab = phpmps_category
        try:
            phpmps_category.create_table()
        except:
            pass

    def getall(self):
        return phpmps_category.select()

    def initial_db(self, post_data):
        phpmps_category.create(
            catid=post_data['catid'][0],
            catname=post_data['catname'],
            parentid=post_data['parentid'],
            catorder=post_data['catorder'],
            weight=post_data['weight'],
        )

    def get_parent_list(self):
        db_data = phpmps_category.select().where(phpmps_category.uid.endswith('00')).order_by(
            phpmps_category.uid)
        return (db_data)

    def get_range2_with_parent(self, parentid):
        db_data = phpmps_category.select().where(phpmps_category.pid == parentid).order_by(phpmps_category.uid)

        return (db_data)

    def get_qian2(self, qian2):
        '''
        用于首页。根据前两位，找到所有的大类与小类。
        并为方便使用，使用数组的形式返回。
        :param qian2: 分类id的前两位
        :return: 数组，包含了找到的分类
        '''

        parentid = qian2 + '00'
        a = phpmps_category.select().where(phpmps_category.uid.startswith(qian2)).order_by(phpmps_category.uid)
        return (a)

    def get_by_id(self, in_uid):
        recs = self.tab.select().where(self.tab.uid == in_uid)

        if recs.count() == 0:
            return None
        else:
            return recs.get()

    def get_range2_without_parent(self, parentid):
        a = phpmps_category.select().where(phpmps_category.uid.startswith(parentid[:2]))
        return (a)

    def get_weight_id(self, catid):
        a = phpmps_category.get(phpmps_category.uid == catid)
        return (a.weight)

    def update(self, uid, post_data, update_time=False):
        if update_time:
            entry = self.tab.update(

                catname=post_data['catname'][0],
                parentid=post_data['parentid'][0],
                weight=post_data['weight'][0],
                catorder=post_data['catorder'][0],
            ).where(self.tab.uid == uid)
        else:
            entry = self.tab.update(

                catname=post_data['catname'][0],
                parentid=post_data['parentid'][0],
                weight=post_data['weight'][0],
                catorder=post_data['catorder'][0],
            ).where(self.tab.uid == uid)
        entry.execute()

    def insert_data(self, post_data):

        entry = self.tab.create(
            catid=post_data['catid'][0],
            catname=post_data['catname'][0],
            parentid=post_data['parentid'][0],
            weight=post_data['weight'][0],
            catorder=post_data['catorder'][0],

        )
        return (entry.catid)

    def query_recent(self, num=8):
        return self.tab.select().order_by(self.tab.order.asc()).limit(num)

    def query_dated(self, num=8):
        return self.tab.select().order_by(self.tab.order.asc()).limit(num)

    def query_random(self, num=6):
        if config.dbtype == 1 or config.dbtype == 3:
            return self.tab.select().order_by(peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return self.tab.select().order_by(peewee.fn.Rand()).limit(num)

    def get_by_uid(self, sig):
        try:
            return self.tab.get(catid=sig)
        except:
            return False

    def delete(self, del_id):
        try:
            del_count = self.tab.delete().where(self.tab.uid == del_id)
            del_count.execute()
            return True
        except:
            return False
