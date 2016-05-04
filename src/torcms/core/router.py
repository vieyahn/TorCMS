# -*- coding:utf-8 -*-


from torcms.torlite.handlers.admin_handler import AdminHandler
from torcms.torlite.handlers.category_handler import CategoryHandler
from torcms.torlite.handlers.entity_handler import EntityHandler
from torcms.torlite.handlers.index import IndexHandler
from torcms.torlite.handlers.label_handler import LabelHandler
from torcms.torlite.handlers.link_handler import LinkHandler, LinkAjaxHandler
from torcms.torlite.handlers.maintain_handler import MaintainCategoryHandler,MaintainCategoryAjaxHandler
from torcms.torlite.handlers.page_handler import PageHandler, PageAjaxHandler
from torcms.torlite.handlers.post2reply_handler import Post2ReplyHandler
from torcms.torlite.handlers.post_handler import PostHandler,PostAjaxHandler
from torcms.torlite.handlers.reply_handler import ReplyHandler
from torcms.torlite.handlers.search_handler import SearchHandler
from torcms.torlite.handlers.user_handler import UserHandler, UserAjaxHandler
from torcms.torlite.handlers.widget_handler import WidgetHandler
from torcms.torlite.handlers.wiki_handler import WikiHandler

urls = [

    ("/label/(.*)", LabelHandler, dict()),
    ("/admin/(.*)", AdminHandler, dict()),
    ("/post/toreply/(.*)", Post2ReplyHandler, dict()),
    ("/entry/(.*)", EntityHandler, dict()),
    ("/category/(.*)", CategoryHandler, dict()),
    ("/user/p/(.*)", UserAjaxHandler, dict()),
    ("/user/(.*)", UserHandler, dict()),
    ("/post/p/(.*)", PostAjaxHandler, dict()),
    ("/post/(.*)", PostHandler, dict()),

    ("/maintain/p/category/(.*)", MaintainCategoryAjaxHandler, dict()),
    ("/maintain/category/(.*)", MaintainCategoryHandler, dict()),
    ("/link/p/(.*)", LinkAjaxHandler, dict()),
    ("/link/(.*)", LinkHandler, dict()),

    ("/page/p/(.*)", PageAjaxHandler, dict()),
    ("/page/(.*)", PageHandler, dict()),
    ("/wiki/(.*)", WikiHandler, dict()),
    ("/search/(.*)", SearchHandler, dict()),
    ("/reply/(.*)", ReplyHandler, dict()),

    ("/widget/(.*)", WidgetHandler, dict(hinfo={})),
    ("/", IndexHandler, dict()),
]
