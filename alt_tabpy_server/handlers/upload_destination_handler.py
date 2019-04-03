import logging
import os
import tornado.web

logger = logging.getLogger(__name__)

_QUERY_OBJECT_STAGING_FOLDER = 'staging'


class UploadDestinationHandler(tornado.web.RequestHandler):
    def initialize(self, app):
        super(UploadDestinationHandler, self).initialize(app)

    def get(self):
        logger.debug(
            'Processing GET for /configurations/endpoint_upload_destination')
        if self.should_fail_with_not_authorized():
            self.fail_with_not_authorized()
            return

        path = self.settings['state_file_path']
        path = os.path.join(path, _QUERY_OBJECT_STAGING_FOLDER)
        self.write({"path": path})
