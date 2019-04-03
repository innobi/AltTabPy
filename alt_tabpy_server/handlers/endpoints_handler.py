'''
HTTP handeler to serve general endpoints request, specifically
http://myserver:9004/endpoints

For how individual endpoint requests are served look
at endpoint_handler.py
'''

import json
import tornado.web


class EndpointsHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(json.dumps(self.tabpy_state.get_endpoints()))

    def post(self):
        if not self.request.body:
            self.send_error(400)
            self.finish()

        request_data = json.loads(self.request.body.decode('utf-8'))

        name = request_data['name']

        # check if endpoint already exist
        if name in self.tabpy_state.get_endpoints():
            self.send_error(400)
            self.finish()

        self._add_or_update_endpoint('add', name, 1, request_data)
