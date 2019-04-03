import json
import logging
import requests
import tornado.web


logger = logging.getLogger(__name__)


class RestrictedTabPy:
    def __init__(self, port):
        self.port = port

    def query(self, name, *args, **kwargs):
        url = f'http://localhost:{self.port}/query/{name}'
        logger.debug(f'Quering {url}...')
        internal_data = {'data': args or kwargs}
        data = json.dumps(internal_data)
        headers = {'content-type': 'application/json'}
        response = requests.post(url=url, data=data, headers=headers,
                                 timeout=30)

        return response.json()


class EvaluationPlaneHandler(tornado.web.RequestHandler):
    '''
    EvaluationPlaneHandler is responsible for running arbitrary python scripts.
    '''

    async def post(self):
        logger.debug('Processing POST for /evaluate')
        if self.should_fail_with_not_authorized():
            self.fail_with_not_authorized()
            return

        self._add_CORS_header()
        try:
            body = json.loads(self.request.body.decode('utf-8'))
            if 'script' not in body:
                self.error_out(400, 'Script is empty.')
                return

            # Transforming user script into a proper function.
            user_code = body['script']
            arguments = None
            arguments_str = ''
            if 'data' in body:
                arguments = body['data']

            if arguments is not None:
                if not isinstance(arguments, dict):
                    self.error_out(400, 'Script parameters need to be '
                                        'provided as a dictionary.')
                    return
                else:
                    arguments_expected = []
                    for i in range(1, len(arguments.keys()) + 1):
                        arguments_expected.append('_arg' + str(i))
                    if sorted(arguments_expected) == sorted(arguments.keys()):
                        arguments_str = ', ' + ', '.join(arguments.keys())
                    else:
                        self.error_out(400, 'Variables names should follow '
                                            'the format _arg1, _arg2, _argN')
                        return

            function_to_evaluate = ('def _user_script(tabpy'
                                    + arguments_str + '):\n')
            for u in user_code.splitlines():
                function_to_evaluate += ' ' + u + '\n'

            logger.info(
                "function to evaluate=%s" % function_to_evaluate)

            result = await self.call_subprocess(function_to_evaluate,
                                                arguments)
            if result is None:
                self.error_out(400, 'Error running script. No return value')
            else:
                self.write(json.dumps(result))
                self.finish()

        except Exception as e:
            err_msg = "%s : " % e.__class__.__name__
            err_msg += "%s" % str(e)
            if err_msg != "KeyError : 'response'":
                err_msg = format_exception(e, 'POST /evaluate')
                self.error_out(500, 'Error processing script', info=err_msg)
            else:
                self.error_out(
                    404,
                    'Error processing script',
                    info="The endpoint you're "
                    "trying to query did not respond. Please make sure the "
                    "endpoint exists and the correct set of arguments are "
                    "provided.")
