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
import tornado.template
import tornado.auth
import tornado.ioloop 
import unicodedata
from tornado.options import define, options
from base64 import b64decode
from crypt  import crypt

config_file = open("config.yml")
config = yaml.load(config_file)
config_file.close()

define("port", default=8888, help="The server is run on the given port.", type=int)

define("apps_dir", default=os.path.join(os.path.dirname(__file__), "apps"), help="The default location where all applications reside")

applications_list = os.listdir(options.apps_dir)
applications_list = [app for app in applications_list if(os.path.isfile(os.path.join(os.path.dirname(__file__), options.apps_dir, app, "config.yml"))
                                                         and os.path.isfile(os.path.join(os.path.dirname(__file__), options.apps_dir, app, "routes.yml"))
                                                         and os.path.isfile(os.path.join(os.path.dirname(__file__), options.apps_dir, app, "__init__.py")))]

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html', title="/", listing=applications_list)

class ResetHandler(tornado.web.RequestHandler):
  def get(self):
    logging.info("Server restart requested. Rebooting server.")
    io_loop = tornado.ioloop.IOLoop.instance()
    for fd in io_loop._handlers.keys():
      try:
        os.close(fd)
      except:
        pass
    os.execv(sys.executable, [sys.executable] + sys.argv) 

#Handling External Applications Starts

handlers = []

for app in applications_list:
  exec('import '+str(options.apps_dir)+'.'+str(app)+'.application')


for app in applications_list:
  routes_file = open(os.path.join(os.path.dirname(__file__), options.apps_dir, app,"routes.yml"))
  routes = yaml.load(routes_file)
  routes_file.close()
  routes = routes['app_route']
  route_handlers = [(r"/"+app+str(v['route']),eval(str(options.apps_dir)+'.'+str(app)+'.application.'+v['handler'])) for i,v in routes.iteritems()]
  handlers = handlers + route_handlers

handlers = handlers + [ 
             (r"/", IndexHandler),
             (r"/reset", ResetHandler),
            ]

print(str(handlers))

settings = {
            'xsrf_cookies': True,
            'cookie_secret':"11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static"),
           }

#Handling External Applications Ends
application_init = tornado.web.Application(handlers, **settings)

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(application_init)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
