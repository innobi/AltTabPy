import argparse

import tornado.ioloop
import tornado.web

from alt_tabpy.handlers import EvaluateHandler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9004)
    args = parser.parse_args()

    app = tornado.web.Application(
        [
            (r'/evaluate', EvaluateHandler),
        ])
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
