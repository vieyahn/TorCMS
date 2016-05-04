__author__ = 'bukun'

raw_text = '''
http://www.yunsuan.org
http://www.yunsuan.org/list/recent
http://www.yunsuan.org/post/recent
'''
import sys
sys.path.append('/opt/torlite/yunsuan')

from torcms.torlite import MPost
from torcms.torlite import MPage
from torcms.torlite import MCatalog
from maplet.model.app2catalog_model import MApp2Catalog
from torcms.torlite import MPost2Catalog

from maplet.model.equation_model import MApp

if __name__ == '__main__':
    uu = MApp()
    tt = uu.get_all()

    vv = MPost()
    ss  = vv.query_all()

    ab = MCatalog()
    ba = ab.query_all()

    cd = MPage()
    dc = cd.query_all()

    with open('site_map_haosou.txt', 'w') as fo:
        fo.write(raw_text)
        for x in tt:
            # print(x.uid)
            fo.write('http://www.yunsuan.org/app/{0}\n'.format(x.uid))
        for y in ss:
            fo.write('http://www.yunsuan.org/post/{0}.html\n'.format(y.uid))

        for z in ba:
            print(z.slug)
            fo.write('http://www.yunsuan.org/tag/{0}\n'.format(z.slug))
            fo.write('http://www.yunsuan.org/category/{0}\n'.format(z.slug))


        for tt in dc:

            if  tt.slug == '':
                pass
            else:
                print(tt.slug)
                fo.write('http://www.yunsuan.org/page/{0}.html\n'.format(tt.slug))