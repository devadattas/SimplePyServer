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
import tornado.template
import tornado.auth
import tornado.ioloop 

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(str(os.listdir("/")))

class TestHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Testing")

