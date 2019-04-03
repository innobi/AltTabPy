import json
import requests
import tornado.web


class EvaluationPlaneHandler(tornado.web.RequestHandler):
    '''
    Class responsible for handling arbitrary scripts from Tableau.

    Assuming the main application assigns this to the /evaluate endpoint,
    scripts executed from Tableau will post to this class.
    '''

    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        user_code = body['script']
        arguments = None
        arguments_str = ''
        if 'data' in body:
            arguments = body['data']

        if arguments is not None:
            arguments_expected = []
            for i in range(1, len(arguments.keys()) + 1):
                arguments_expected.append('_arg' + str(i))

            if sorted(arguments_expected) == sorted(arguments.keys()):
                arguments_str = ', ' + ', '.join(arguments.keys())

        function_to_evaluate = ('def _user_script(tabpy'
                                + arguments_str + '):\n')
        for u in user_code.splitlines():
            function_to_evaluate += ' ' + u + '\n'

        breakpoint()
        result = 1
        if result is None:
            self.error_out(400, 'Error running script. No return value')
        else:
            self.write(json.dumps(result))
            self.finish()
