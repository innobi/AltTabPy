import logging
import os
import sys
import shutil
from re import compile as _compile
from uuid import uuid4 as random_uuid

from alt_tabpy_server.handlers import MainHandler
from alt_tabpy_server.handlers.base_handler import STAGING_THREAD
from alt_tabpy_server.management.state import get_query_object_path
from alt_tabpy_server.psws.callbacks import on_state_change


def copy_from_local(localpath, remotepath, is_dir=False):
    if is_dir:
        if not os.path.exists(remotepath):
            # remote folder does not exist
            shutil.copytree(localpath, remotepath)
        else:
            # remote folder exists, copy each file
            src_files = os.listdir(localpath)
            for file_name in src_files:
                full_file_name = os.path.join(localpath, file_name)
                if os.path.isdir(full_file_name):
                    # copy folder recursively
                    full_remote_path = os.path.join(remotepath, file_name)
                    shutil.copytree(full_file_name, full_remote_path)
                else:
                    # copy each file
                    shutil.copy(full_file_name, remotepath)
    else:
        shutil.copy(localpath, remotepath)


class ManagementHandler(MainHandler):
    def initialize(self, app):
        super(ManagementHandler, self).initialize(app)
        self.port = self.settings['port']

    def _get_protocol(self):
        return 'http://'

    async def _add_or_update_endpoint(self, action, name, version, request_data):
        '''
        Add or update an endpoint
        '''
        logging.debug("Adding/updating model {}...".format(name))
        _name_checker = _compile('^[a-zA-Z0-9-_\\s]+$')
        if not isinstance(name, str):
            raise TypeError("Endpoint name must be a string")

        if not _name_checker.match(name):
            return ('endpoint name can only contain: a-z, A-Z, 0-9,'
                    ' underscore, hyphens and spaces.')

        if self.settings.get('add_or_updating_endpoint'):
            raise RuntimeError("Another endpoint update is already in progress"
                               ", please wait a while and try again")

        request_uuid = random_uuid()
        self.settings['add_or_updating_endpoint'] = request_uuid
        try:
            description = (request_data['description']
                           if 'description' in request_data else None)
            if 'docstring' in request_data:
                if sys.version_info > (3, 0):
                    docstring = str(bytes(request_data['docstring'],
                                          "utf-8").decode('unicode_escape'))
                else:
                    docstring = request_data['docstring'].decode(
                        'string_escape')
            else:
                docstring = None
            endpoint_type = (request_data['type'] if 'type' in request_data
                             else None)
            methods = (request_data['methods'] if 'methods' in request_data
                       else [])
            dependencies = (request_data['dependencies']
                            if 'dependencies' in request_data else None)
            target = (request_data['target']
                      if 'target' in request_data else None)
            schema = (request_data['schema'] if 'schema' in request_data
                      else None)

            src_path = (request_data['src_path'] if 'src_path' in request_data
                        else None)
            target_path = get_query_object_path(
                self.settings['state_file_path'], name, version)
            _path_checker = _compile('^[\\a-zA-Z0-9-_\\s/]+$')
            # copy from staging
            if src_path:
                if not isinstance(request_data['src_path'], str):
                    return "src_path must be a string."
                if not _path_checker.match(src_path):
                    return ('Endpoint name can only contain: a-z, A-'
                            'Z, 0-9,underscore, hyphens and spaces.')

                await self._copy_po_future(src_path, target_path)
            elif endpoint_type != 'alias':
                return "src_path is required to add/update an endpoint."

            # alias special logic:
            if endpoint_type == 'alias':
                if not target:
                    return 'Target is required for alias endpoint.'
                dependencies = [target]

            # update local config
            try:
                if action == 'add':
                    self.tabpy_state.add_endpoint(
                        name=name,
                        description=description,
                        docstring=docstring,
                        endpoint_type=endpoint_type,
                        methods=methods,
                        dependencies=dependencies,
                        target=target,
                        schema=schema)
                else:
                    self.tabpy_state.update_endpoint(
                        name=name,
                        description=description,
                        docstring=docstring,
                        endpoint_type=endpoint_type,
                        methods=methods,
                        dependencies=dependencies,
                        target=target,
                        schema=schema,
                        version=version)

            except Exception as e:
                return "Error when changing TabPy state: %s" % e

            on_state_change(self.settings,
                            self.tabpy_state,
                            self.python_service)

        finally:
            self.settings['add_or_updating_endpoint'] = None

    async def _copy_po_future(self, src_path, target_path):
        future = STAGING_THREAD.submit(copy_from_local, src_path,
                                       target_path, is_dir=True)
        ret = await future
        return ret
