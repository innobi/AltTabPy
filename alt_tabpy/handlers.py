import ast
import json
import textwrap
from typing import Callable, Dict, List

import tornado.escape
import tornado.web


class EvaluateHandler(tornado.web.RequestHandler):
    '''
    Class responsible for handling arbitrary scripts from Tableau.

    Assuming the main application assigns this to the /evaluate endpoint,
    scripts executed from Tableau will post to this class.
    '''

    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        user_code = body['script']
        kwargs = body.get('data', {})

        func = self._func_from_request_parts(user_code, list(kwargs.keys()))
        result = func(**kwargs)

        self.write(json.dumps(result))

    @classmethod
    def _func_from_request_parts(cls,
                                 user_code: str,
                                 arg_names: List[str]) -> Callable:
        func_name = 'foo'  # arbitrary; used to look up injection in namespace
        indented = textwrap.indent(user_code, ' ' * 4)  # Follow PEP8 style
        arguments = ', '.join(arg_names)
        expr = f"def {func_name}({arguments}):\n{indented}"
        mod_ast = ast.parse(expr)

        # Inject the function into an arbitrary namespace
        dummy: Dict[str, Callable] = {}
        code = compile(mod_ast, 'also_arbitrary', mode='exec')
        exec(code, dummy)

        return dummy[func_name]
