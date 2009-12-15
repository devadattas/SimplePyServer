class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(str(os.listdir("/")))

class TestHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Testing")

