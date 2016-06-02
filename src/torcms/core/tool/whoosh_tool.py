# -*- coding:utf-8 -*-

from whoosh.index import open_dir
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser
from whoosh.query import *

analyzer = ChineseAnalyzer()
ix = open_dir("database/whoosh")
parser = QueryParser("content", schema=ix.schema)


class yunsearch():
    def get_all_num(self, keyword, catid=''):
        q = parser.parse(keyword)
        if catid== '':
            pass
        else:
            q = And([Term("catid", catid), q])
        return len(ix.searcher().search(q).docs())

    def search(self, keyword, limit=20):
        q = parser.parse(keyword)
        try:
            tt = ix.searcher().search(q, limit=limit)
            return (tt)
        finally:
            pass


    def search_pager(self, keyword,  catid = '',page_index=1, doc_per_page=10):
 
        q = parser.parse(keyword)
        if catid == '':
            pass
        else:
            q = And([Term("catid",catid),q ])
        try:
            tt = ix.searcher().search(q, limit=page_index * doc_per_page)
            return (tt[(page_index - 1) * doc_per_page: page_index * doc_per_page])
        finally:
            pass



       
