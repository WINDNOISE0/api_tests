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
            Logger.info("")
            Logger.info(f"=====================    Response    =====================")
            Logger.info(f"Status code: '{response.status_code}', elapsed_time='{response.elapsed}']")
            Logger.info(f"---------------------------body---------------------------")
            Logger.info(f"{body}")
            Logger.info(f"----------------------------------------------------------\n\n\n")
            return response

        return _log_response
