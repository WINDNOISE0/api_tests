from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.models.register_request import RegisterRequest
from services.auth.helpers.user_helper import UserHelper
from services.auth.models.login_request import LoginRequest
from services.auth.models.login_response import LoginResponse
from services.base_service import BaseService

from services.university.models.success_response import SuccessResponse
from utils.api_utils import ApiUtils


class AuthService(BaseService):
    SERVICE_URL = "http://localhost:8000"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.authorization_helper = AuthorizationHelper(self.api_utils)
        self.user_helper = UserHelper(self.api_utils)

    def register_user(self, register_request: RegisterRequest) -> SuccessResponse:
        response = self.authorization_helper.post_register(data=register_request.model_dump())
        return SuccessResponse(**response.json())

    def login_user(self, login_request: LoginRequest) -> LoginResponse:
        response = self.authorization_helper.post_login(data=login_request.model_dump())
        return LoginResponse(**response.json())
