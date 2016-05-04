# -*- coding:utf-8 -*-

from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.claslite.model.catalog_model import MCatalog as MPycateMCatalog
from torcms.claslite.model.infor_model import MInfor
from torcms.torlite.model.mcatalog import MCatalog
from torcms.torlite.model.mpost import MPost


class PycateIndexHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.mpycate = MPycateMCatalog()
        self.minfo = MInfor()

    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html')

    def index(self):
        cstr = tools.get_uuid()
        self.set_cookie('user_pass', cstr)

        t1 = self.mpycate.get_qian2('01')
        s1 = self.format_cat(t1, 1)
        t2 = self.mpycate.get_qian2('02')
        s2 = self.format_cat(t2, 2)
        t3 = self.mpycate.get_qian2('03')
        s3 = self.format_cat(t3, 3)
        t4 = self.mpycate.get_qian2('04')
        s4 = self.format_cat(t4, 4)
        t5 = self.mpycate.get_qian2('05')
        s5 = self.format_cat(t5, 5)
        t6 = self.mpycate.get_qian2('06')
        s6 = self.format_cat(t6, 6)

        kwd = {
            's1': s1,
            's2': s2,
            's3': s3,
            's4': s4,
            's5': s5,
            's6': s6,

            'parentid': '0000',
            'parentlist': self.mpycate.get_parent_list(),
            'cookie_str': cstr

        }

        self.render('index/index.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    catalog_info=self.mcat.query_all(by_order=True),
                    view=self.mpost.query_most_pic(20),
                    )

    def format_cat(self, input, sig):
        '''
        根据分类，生成不同的区域
        '''

        headstr = '''<div class="panel panel-info" style="width:90%"><div class="panel-heading">
        <span class="glyphicon glyphicon-th-large"></span>
                <span id="title_{sig1}"></span>
                <span><a href='/list/{catid1}'>{catname1}</a></span>
              </div>
                <ul class="list-group">
                '''

        outstr = ''

        for rec_cat in input:
            # 记录的数目
            if rec_cat.uid.endswith('00'):
                headstr = headstr.format(sig1=sig, catid1=rec_cat.uid, catname1=rec_cat.name)
                continue
            recout = self.minfo.get_cat_recs_count(rec_cat.uid)
            if recout > 0:
                recout = str(recout)
            else:
                recout = 0
            tmpstr = '''<li class="list-group-item">
                    <a href="/list/{scatid}" title="{scatname}">{scatname}</a>
                    <span style="color:#666;font-size:12px">({scount})</span></li>
                    '''.format(scatid=rec_cat.uid, scatname=rec_cat.name, scount=recout)
            outstr += tmpstr

        outstr += '''</ul></div>'''
        outstr = headstr + outstr
        return (outstr)
