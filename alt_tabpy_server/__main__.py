import tornado.ioloop
import tornado.web

from alt_tabpy_server.handlers import EvaluateHandler

PORT = 9004


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r'/evaluate', EvaluateHandler),
        ])
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
