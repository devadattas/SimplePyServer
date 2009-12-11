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

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"", IndexHandler),
      (r""+ "/", IndexHandler),
      (r""+ "/(.+)", IndexHandler),
      ]
    settings = dict(
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      xsrf_cookies=True,
      cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    )
    tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
  @property
  def db(self):
    return self.application.db

class IndexHandler(BaseHandler):
  def get(self,route=""):
    self.write('Let\'s Start');

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
