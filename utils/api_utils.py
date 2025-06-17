from requests import Session

import json
from logger.logger import Logger
from utils.json_utils import JsonUtils

import curlify
import requests

class LoggerUtils:
    @staticmethod
    def log_response(func):
        def _log_response(*args, **kwargs) -> requests.Response:
            response = func(*args, **kwargs)
            Logger.info(f"=====================    Request    =====================")
            Logger.info(f"ENDPOINT: {response.url}")
            Logger.info(f"{curlify.to_curl(response.request)}")
            Logger.info(f"Headers request: \n{response.headers}")
            body = json.dumps(response.json(), indent=2) if JsonUtils.is_json(response.text) else response.text

            Logger.info(f"=====================    Response    =====================")
            Logger.info(f"Status code: '{response.status_code}', elapsed_time='{response.elapsed}']")
            Logger.info(f"---------------------------body---------------------------")
            Logger.info(f"{body}")
            Logger.info(f"----------------------------------------------------------\n\n\n")
            return response
        return _log_response


class ApiUtils:
    log_response = staticmethod(LoggerUtils.log_response)

    def __init__(self, url, headers=None):
        if headers is None:
            headers = {}

        self.url = url

        self.session = Session()
        self.session.headers = headers

    @log_response
    def get(self, endpoint_url, **kwargs):
        response = self.session.get(self.url + endpoint_url, **kwargs)
        return response

    @log_response
    def post(self, endpoint_url, data=None, json=None, **kwargs):
        response = self.session.post(self.url + endpoint_url, data=data, json=json, **kwargs)
        return response
