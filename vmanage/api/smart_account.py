# Created by robhugh on 10 February 2022 on behalf of Cisco Systems, Inc.

"""Cisco vManage Device Templates API Methods.
"""

import json
import re
from vmanage.api.feature_templates import FeatureTemplates
from vmanage.api.http_methods import HttpMethods
from vmanage.data.parse_methods import ParseMethods
from vmanage.utils import list_to_dict
from vmanage.api.utilities import Utilities


class SmartAccount(object):
    """vManage Smart Account API
    Responsible for DELETE, GET, POST, PUT methods against vManage
    Device Templates.
    """
    def __init__(self, session, host, port=443):
        """Initialize Device Templates object with session parameters.
        Args:
            session (obj): Requests Session object
            host (str): hostname or IP address of vManage
            port (int): default HTTPS 443
        """

        self.session = session
        self.host = host
        self.port = port
        self.base_url = f'https://{self.host}:{self.port}/dataservice/'

    def sync_smart_account(self, username, password):
        """Syncs the given smart account

        Args:
            username (string): the username of the smart account
            password (string): the password of the smart account
        """

        url = f"{self.base_url}system/device/smartaccount/sync"
        payload = {"username": username, "password": password, "env": '', "organization_name": '', "validity_string": 'valid'}
        response = HttpMethods(self.session, url).request('POST', payload=json.dumps(payload))
        print(response)
