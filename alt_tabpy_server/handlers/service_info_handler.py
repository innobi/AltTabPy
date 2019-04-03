import json
import tornado.web

class ServiceInfoHandler(tornado.web.RequestHandler):

    def get(self):
        info = {}
        info['description'] = "Revamped Alt Tabpy Server"
        self.write(json.dumps(info))
