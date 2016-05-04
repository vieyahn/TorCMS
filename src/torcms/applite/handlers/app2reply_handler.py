# -*- coding:utf-8 -*-

from torcms.torlite.model.mreply import MReply
from torcms.torlite.model.mreply2user import MReply2User
from torcms.applite.model.app_reply_model import MApp2Reply
from torcms.torlite.handlers.post2reply_handler import Post2ReplyHandler


class App2ReplyHandler(Post2ReplyHandler):
    def initialize(self):
        self.init()
        self.mreply = MReply()
        self.mreply2user = MReply2User()
        self.mpost2reply = MApp2Reply()



