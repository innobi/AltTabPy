import tornado.ioloop
import tornado.web

from alt_tabpy_server.handlers import EvaluationPlaneHandler, ServiceInfoHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


PORT = 9004


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r'/info', ServiceInfoHandler),
            (r'/evaluate', EvaluationPlaneHandler),
        ])
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
