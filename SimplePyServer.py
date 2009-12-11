# -*- coding: utf-8 -*-
import inspect
import logging
import os.path
import re
import sys
import yaml
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import unicodedata
from tornado.options import define, options

config_file = open("config.yml")
config = yaml.load(config_file)
config_file.close()

define("port", default=8888, help="The server is run on the given port.", type=int)
define("document_root",default=config['server_configuration']['document_root'], help="This is the document root for the server.", type=str)

handlers = [ 
             (r"/", IndexHandler),
             (r"/reset", ResetHandler),
             (r"/static", ResetHandler),
            ]
application_init = tornado.web.Application()


