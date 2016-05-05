# -*- coding:utf-8 -*-

import torcms.handlers.info_handler
import torcms.handlers.info_list_handler
import torcms.handlers.info_publish_handler
from torcms.handlers.info_tag_hanler import InfoTagHandler
from torcms.claslite.handlers.maintain_handler import MaintainPycateCategoryHandler
from torcms.handlers.meta_handler import MetaHandler
from torcms.handlers.admin_handler import AdminHandler
from torcms.handlers.category_handler import CategoryHandler
from torcms.handlers.entity_handler import EntityHandler
from torcms.handlers.index import IndexHandler
from torcms.handlers.label_handler import LabelHandler
from torcms.handlers.link_handler import LinkHandler, LinkAjaxHandler
from torcms.handlers.maintain_handler import MaintainCategoryHandler,MaintainCategoryAjaxHandler
from torcms.handlers.page_handler import PageHandler, PageAjaxHandler
from torcms.handlers.post2reply_handler import Post2ReplyHandler
from torcms.handlers.reply_handler import ReplyHandler
from torcms.handlers.search_handler import SearchHandler
from torcms.handlers.user_handler import UserHandler, UserAjaxHandler
from torcms.handlers.widget_handler import WidgetHandler
from torcms.handlers.wiki_handler import WikiHandler
from torcms.handlers.post_handler import PostHandler,PostAjaxHandler

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

    ('/meta/(.*)', MetaHandler, dict()),
    ("/info/(.*)", torcms.handlers.info_handler.InfoHandler, dict(hinfo={})),
    ("/maintain/claslitecategory/(.*)", MaintainPycateCategoryHandler, dict()),
    ("/list/(.*)", torcms.handlers.info_list_handler.InfoListHandler, dict(hinfo={})),
    ("/publish/(.*)", torcms.handlers.info_publish_handler.InfoPublishHandler, dict(hinfo={})),
    ('/info_tag/(.*)', InfoTagHandler, dict(hinfo={})),
    ("/", IndexHandler, dict()),

]
