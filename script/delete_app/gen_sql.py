__author__ = 'bukun'


tepl = '''
delete from tabusage WHERE signature_id = "{0}";
delete from tabapp2label WHERE app_id = "{0}";
delete from tabevaluation WHERE app_id = "{0}";
delete from tabcollect WHERE app_id = "{0}";
delete from tabapp WHERE uid = "{0}";
'''

app_arr = ['0376', '0377']


with open('out.sql','w') as fo:
    for app in app_arr:
        uu = tepl.format(app)
        fo.write(uu)
