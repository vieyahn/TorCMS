# -*- coding:utf-8 -*-


import uuid
import random
import tornado
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from bs4 import BeautifulSoup
import time
import hashlib


def md5(instr):
    return hashlib.md5(instr.encode('utf-8')).hexdigest()


def timestamp():
    return int(time.time())


def format_yr(indate):
    return indate.strftime('%m-%d')


def format_date(indate):
    return indate.strftime('%Y-%m-%d %H:%M:%S')


def get_uuid():
    return str(uuid.uuid1())


def get_uu8d():
    return (str(uuid.uuid1()).split('-')[0])


def get_uu4d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 4)
    return (''.join(slice))


def get_uu5d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 5)
    return (''.join(slice))


def get_uudd(lenth):
    '''
    随机获取给定位数的整数
    :param lenth:
    :return:
    '''
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    slice = random.sample(sel_arr, lenth)
    while slice[0] == '0':
        slice = random.sample(sel_arr, lenth)
    return (int(''.join(slice)))


def get_uu6d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 6)
    return (''.join(slice))


def markdown2html(markdown_text):
    html = markdown.markdown(markdown_text,
                             extensions=[WikiLinkExtension(base_url='/wiki/', end_url=''),
                                         'markdown.extensions.extra',
                                         'markdown.extensions.toc',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.meta',
                                         ])
    return tornado.escape.xhtml_escape(html)



##  弃用的函数
def gen_pager_bootstrap_url(cat_slug, page_num, current):
    # cat_slug 分类
    # page_num 页面总数
    # current 当前页面
    if page_num == 1:
        return ''

    pager_shouye = '''
    <li class="{0}">
    <a href="{1}/{2}">&lt;&lt; 首页</a>
                </li>'''.format('hidden' if current <= 1 else '', cat_slug, current)

    pager_pre = '''
                <li class="{0}">
                <a href="{1}/{2}">&lt; 前页</a>
                </li>
                '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''
                <li class="{0}">
                <a  href="{1}/{2}">{2}</a></li>
                '''.format('active' if ind + 1 == current else '', cat_slug, ind + 1)
        pager_mid += tmp_mid
    pager_next = '''
                <li class=" {0}">
                <a  href="{1}/{2}">后页 &gt;</a>
                </li>
                '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
    pager_last = '''
                <li class=" {0}">
                <a href="{1}/{2}">末页
                    &gt;&gt;</a>
                </li>
                '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return (pager)


##  弃用的函数
def gen_pager_purecss(cat_slug, page_num, current):
    # cat_slug 分类
    # page_num 页面总数
    # current 当前页面
    if page_num == 1:
        return ''

    pager_shouye = '''
    <li class="pure-menu-item {0}">
    <a class="pure-menu-link" href="{1}">&lt;&lt; 首页</a>
                </li>'''.format('hidden' if current <= 1 else '', cat_slug)

    pager_pre = '''
                <li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">&lt; 前页</a>
                </li>
                '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''
                <li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">{2}</a></li>
                '''.format('selected' if ind + 1 == current else '', cat_slug, ind + 1)
        pager_mid += tmp_mid
    pager_next = '''
                <li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">后页 &gt;</a>
                </li>
                '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
    pager_last = '''
                <li class="pure-menu-item {0}">
                <a hclass="pure-menu-link" ref="{1}/{2}">末页
                    &gt;&gt;</a>
                </li>
                '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return (pager)
