from requests import Session

from utils.logger_utils import LoggerUtils


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
