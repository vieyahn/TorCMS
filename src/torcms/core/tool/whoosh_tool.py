# -*- coding:utf-8 -*-


# from whoosh.fields import *
from whoosh.index import open_dir
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser

analyzer = ChineseAnalyzer()
ix = open_dir("database/whoosh")
parser = QueryParser("content", schema=ix.schema)


class yunsearch():
    def get_all_num(self, keyword):
        q = parser.parse(keyword)
        return len(ix.searcher().search(q).docs())

    def search(self, keyword, limit=20):
        q = parser.parse(keyword)
        try:
            tt = ix.searcher().search(q, limit=limit)
            return (tt)
        finally:
            pass
            # Don't close the searcher.
            # searcher1.close()

    def search_pager(self, keyword, page_index=1, doc_per_page=10):
        q = parser.parse(keyword)
        try:
            tt = ix.searcher().search(q, limit=page_index * doc_per_page)
            return (tt[(page_index - 1) * doc_per_page: page_index * doc_per_page])
        finally:
            pass
