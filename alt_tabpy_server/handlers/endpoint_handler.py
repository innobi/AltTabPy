'''
HTTP handeler to serve specific endpoint request like
http://myserver:9004/endpoints/mymodel

For how generic endpoints requests is served look
at endpoints_handler.py
'''

import json
import logging
from alt_tabpy_server.management.state import get_query_object_path
import tornado.web


logger = logging.getLogger(__name__)


class EndpointHandler(tornado.web.RequestHandler):

    async def get(self, endpoint_name):
        if not endpoint_name:
            self.write(json.dumps(self.tabpy_state.get_endpoints()))
        else:
            if endpoint_name in self.tabpy_state.get_endpoints():
                self.write(json.dumps(
                    self.tabpy_state.get_endpoints()[endpoint_name]))
            else:
                self.send_error(404)  # 'Unknown endpoint',

        self.finish()

    async def put(self, name):
        if not self.request.body:
            self.send_error(400)  # "Input body cannot be empty"
            self.finish()

        request_data = json.loads(self.request.body.decode('utf-8'))

        # check if endpoint exists
        endpoints = self.tabpy_state.get_endpoints(name)
        if len(endpoints) == 0:
            self.error_out(404,
                           "endpoint %s does not exist." % name)
            self.finish()
            return

        new_version = int(endpoints[name]['version']) + 1
        logger.info('Endpoint info: %s' % request_data)
        err_msg = yield self._add_or_update_endpoint(
            'update', name, new_version, request_data)
        if err_msg:
            self.error_out(400, err_msg)
            self.finish()
        else:
            self.write(self.tabpy_state.get_endpoints(name))
            self.finish()

    async def delete(self, name):
        endpoints = self.tabpy_state.get_endpoints(name)
        if len(endpoints) == 0:
            self.send_error(404)  # endpoint doesn't exist
            self.finish()

        # update state
        endpoint_info = self.tabpy_state.delete_endpoint(name)

        # delete files
        if endpoint_info['type'] != 'alias':
            delete_path = get_query_object_path(
                self.settings['state_file_path'], name, None)

            await self._delete_po_future(delete_path)

        self.set_status(204)
        self.finish()

    async def _delete_po_future(self, delete_path):
        raise NotImplementedError
        # future = STAGING_THREAD.submit(shutil.rmtree, delete_path)
        # ret = await future
        # return ret
