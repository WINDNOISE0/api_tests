import requests

from services.general.helpers.base_helpers import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    PATH_PARAM_ENDPOINT = f"{ENDPOINT_PREFIX}/" + "{}/"

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ENDPOINT_PREFIX, json=json)
        return response
