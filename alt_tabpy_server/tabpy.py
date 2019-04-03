import tornado.ioloop
import tornado.web

from tabpy_server.handlers import (EndpointHandler, EndpointsHandler,
                                   EvaluationPlaneHandler, QueryPlaneHandler,
                                   ServiceInfoHandler, StatusHandler,
                                   UploadDestinationHandler)


if __name__ == '__main__':
    app = tornado.Web.Application(
        [
            # skip MainHandler to use StaticFileHandler .* page requests and
            # default to index.html
            # (r"/", MainHandler),
            (r'/query/([^/]+)', QueryPlaneHandler),
            (r'/status', StatusHandler),
            (r'/info', ServiceInfoHandler),
            (r'/endpoints', EndpointsHandler),
            (r'/endpoints/([^/]+)?', EndpointHandler),
            (r'/evaluate', EvaluationPlaneHandler),
            (r'/configurations/endpoint_upload_destination',
             UploadDestinationHandler)
            (r'/(.*)', tornado.web.StaticFileHandler)
        ])
    app.listen(9004)
    tornado.ioloop.IOLoop.current().start()
