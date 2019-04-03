import json
import logging
import tornado.web


logger = logging.getLogger(__name__)


class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        if self.should_fail_with_not_authorized():
            self.fail_with_not_authorized()
            return

        self._add_CORS_header()

        logger.debug("Obtaining service status")
        status_dict = {}
        for k, v in self.python_service.ps.query_objects.items():
            status_dict[k] = {
                'version': v['version'],
                'type': v['type'],
                'status': v['status'],
                'last_error': v['last_error']}

        logger.debug("Found models: {}".format(status_dict))
        self.write(json.dumps(status_dict))
        self.finish()
        return
