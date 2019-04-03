import json
import tornado.web


class StatusHandler(tornado.web.RequestHandler):

    async def get(self):
        status_dict = {}
        for k, v in self.python_service.ps.query_objects.items():
            status_dict[k] = {
                'version': v['version'],
                'type': v['type'],
                'status': v['status'],
                'last_error': v['last_error']}

        self.write(json.dumps(status_dict))
        self.finish()
