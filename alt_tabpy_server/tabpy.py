import tornado.ioloop
import tornado.web

from alt_tabpy_server.handlers import (
    EndpointHandler, EndpointsHandler, EvaluationPlaneHandler,
    QueryPlaneHandler, ServiceInfoHandler, StatusHandler,
    UploadDestinationHandler)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


PORT = 9004


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r'/query/([^/]+)', QueryPlaneHandler),
            (r'/status', StatusHandler),
            (r'/info', ServiceInfoHandler),
            (r'/endpoints', EndpointsHandler),
            (r'/endpoints/([^/]+)?', EndpointHandler),
            (r'/evaluate', EvaluationPlaneHandler),
            (r'/configurations/endpoint_upload_destination',
             UploadDestinationHandler),
            (r'/(.*)', tornado.web.StaticFileHandler),
        ])
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
