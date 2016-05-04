# -*- coding:utf-8 -*-

import tornadoredis
import tornado.web
import tornado.escape

c = tornadoredis.Client()
c.connect()


class IndexHandler():


    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def index(self):

        self.set_cookie('user_pass', cstr)
        kwd = {
            'cookie_str': cstr
        }
        mapp = torapp.model.app_model.MApp()
        all_cats = mapp.query_most_by_cat(10 ,1)
        # out_str =  self.render_string('extends/modules/list_equation_by_cat.html', recs=all_cats).decode('utf-8')
        # print(out_str)
        yield  tornado.gen.Task(c.set, 'food3','welcome')
        # foo2 = yield tornado.gen.Task(c.get, 'food')

        self.render('tplite/index/index.html',
                    kwd = kwd,
                    userinfo=self.userinfo,
                    catalog_info  = self.mcat.query_all( by_order=True),
                    foo = foo2,
                    unescape = tornado.escape.xhtml_unescape,
                    )

if __name__ == '__main__':
    uu = IndexHandler()
    uu.index()