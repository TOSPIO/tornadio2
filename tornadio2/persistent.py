# -*- coding: utf-8 -*-
"""
    tornadio.persistent
    ~~~~~~~~~~~~~~~~~~~

    Persistent transport implementations.

    :copyright: (c) 2011 by the Serge S. Koval, see AUTHORS for more details.
    :license: Apache, see LICENSE for more details.
"""
import logging

import tornado
from tornado.websocket import WebSocketHandler

class WebSocketHandler(WebSocketHandler):
    def initialize(self, server):
        logging.debug('Initializing FlashSocket handler...')

        self.server = server

    def open(self, version, session_id):
        # TODO: Version check
        self.session = server.get_session(session_id)
        if self.session is None:
            raise tornado.HTTPError(404, "Invalid Session")

        self.session.set_handler(self)

    def on_message(self, message):
        self.async_callback(self.session.raw_message)(message)

    def on_close(self):
        if self.session is not None:
            self.session.close()

    def send(self, messages):
        for m in messages:
            self.write_message(m)

class FlashSocketHandler(WebSocketHandler):
    def initialize(self, server):
        logging.debug('Initializing FlashSocket handler...')

        super(FlashSocketHandler, self).initialize(server)