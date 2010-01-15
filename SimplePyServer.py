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
settings = {}
ignore_apps = []
for app in applications_list:
  exec('\
try:\n\
  import ' + str(options.apps_dir) + '.' + str(app) + '.application\n\
except StandardError, err:\n\
  ignore_apps.append(app)\n\
  print("Server encountered error with: ' + str(options.apps_dir) + '.' + str(app) + '.application.Ignoring this application...")\n\
  print("Error:\\n\t\t"+str(err))')

applications_list = list(set(applications_list).difference(set(ignore_apps)))
print("Booting SimplePyServer...")
print("Applications loaded into memory: " + ", ".join(applications_list))

for app in applications_list:
  routes_file = open(os.path.join(os.path.dirname(__file__), options.apps_dir, app, "routes.yml"))
  app_routes = yaml.load(routes_file)
  routes_file.close()
  routes = app_routes['app_route']
  route_handlers = [(r"/" + app + str(v['route']), eval(str(options.apps_dir) + '.' + str(app) + '.application.' + v['handler'])) for i, v in routes.iteritems()]
  if(app_routes.has_key("static_route")):
    static_route = app_routes['static_route']
    route_handlers = route_handlers + [(r"/" + app + static_route['route'], tornado.web.StaticFileHandler, { 'path' : os.path.join(os.getcwd(), options.apps_dir, app, static_route['path']) })]
  handlers = handlers + route_handlers

handlers = handlers + [ 
             (r"/", IndexHandler),
             (r"/reset", ResetHandler),
            ]

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
