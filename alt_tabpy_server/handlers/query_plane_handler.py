import tornado.web
import logging
from alt_tabpy_server.common.messages import (
    Query, QuerySuccessful, QueryError, UnknownURI)
from hashlib import md5
import uuid
import urllib

from typing import Dict, Tuple, Type


logger = logging.getLogger(__name__)


def _get_uuid():
    """Generate a unique identifier string"""
    return str(uuid.uuid4())


class QueryPlaneHandler(tornado.web.RequestHandler):

    def _query(self,
               po_name: str,
               data: Dict,
               uid: str,
               qry: str) -> Tuple[Type, Dict]:
        """
        Parameters
        ----------
        po_name : str
            The name of the query object to query

        data : dict
            The deserialized request body

        uid: str
            A unique identifier for the request

        qry: str
            The incoming query object. This object maintains
            raw incoming request, which is different from the sanitied data

        Returns
        -------
        out : result type, dict
            A triple containing a result type, the result message
            as a dictionary.
        """
        response = self.python_service.ps.query(po_name, data, uid)

        if isinstance(response, QuerySuccessful):
            response_json = response.to_json()
            self.set_header("Etag", '"%s"' % md5(response_json.encode(
                'utf-8')).hexdigest())
            return QuerySuccessful, response.for_json()
        else:
            logger.error("Failed query, response: {}".format(response))
            return type(response), response.for_json()

    def _handle_result(self, po_name, data, qry, uid):
        (response_type, response, gls_time) = \
            self._query(po_name, data, uid, qry)

        if response_type == QuerySuccessful:
            result_dict = {
                'response': response['response'],
                'version': response['version'],
                'model': po_name,
                'uuid': uid
            }
            self.write(result_dict)
            self.finish()
        elif response_type == UnknownURI:
            self.send_error(404)
        elif response_type == QueryError:
            self.send_error(400)
        else:
            self.send_error()

    def _process_query(self, endpoint_name: str):
        po_name, _ = self._get_actual_model(endpoint_name)

        # po_name is None if self.python_service.ps.query_objects.get(
        # endpoint_name) is None
        if not po_name:
            self.send_error(404)  # endpoint doesn't exist

        po_obj = self.python_service.ps.query_objects.get(po_name)

        if not po_obj:
            self.send_error(404)  # endpoint doesn't exist

        uid = _get_uuid()

        # record query w/ request ID in query log
        qry = Query(po_name, request_json)
        # send a query to PythonService and return
        self._handle_result(po_name, data, qry, uid)

    def _get_actual_model(self, endpoint_name):
        # Find the actual query to run from given endpoint
        all_endpoint_names = []

        while True:
            endpoint_info = self.python_service.ps.query_objects.get(
                endpoint_name)
            if not endpoint_info:
                return [None, None]

            all_endpoint_names.append(endpoint_name)

            endpoint_type = endpoint_info.get('type', 'model')

            if endpoint_type == 'alias':
                endpoint_name = endpoint_info['endpoint_obj']
            elif endpoint_type == 'model':
                break
            else:
                self.error_out(500, 'Unknown endpoint type',
                               info="Endpoint type '%s' does not exist"
                                    % endpoint_type)
                return

        return (endpoint_name, all_endpoint_names)

    def get(self, endpoint_name):
        endpoint_name = urllib.parse.unquote(endpoint_name)
        self._process_query(endpoint_name)

    def post(self, endpoint_name):
        self.send_error()  # Not Implemented...
