# import json
# from logger.logger import Logger
# from json_utils import JsonUtils
#
# import curlify
# import requests
#
# class LoggerUtils:
#     @staticmethod
#     def log_response(func):
#         def _log_response(*args, **kwargs) -> requests.Response:
#             response = func(*args, **kwargs)
#             Logger.info(f"Request: {curlify.to_curl(response.request)}")
#             body = json.dumps(response.json(), indent=2) if JsonUtils.is_json(response.text) else response.text
#             Logger.info(f"Response status code: '{response.status_code}', elapsed_time='{response.elapsed}']\n{body}\n")
#             return response
#         return _log_response
