import argparse

import tornado.ioloop
import tornado.web

from alt_tabpy.handlers import EvaluateHandler, InfoHandler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9004)
    args = parser.parse_args()

    app = tornado.web.Application(
        [
            (r'/info', InfoHandler),
            (r'/evaluate', EvaluateHandler),
        ])
    app.listen(args.port)
    print(f"Listening on port {args.port}!")
    tornado.ioloop.IOLoop.current().start()
