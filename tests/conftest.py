import os

import pytest
from dotenv import load_dotenv

from services.auth.auth_service import AuthService
from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.models.register_request import RegisterRequest
from services.auth.models.login_request import LoginRequest
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.university_service import UniversityService
from test_data.token_data import TokenData
from utils.api_utils import ApiUtils
from faker import Faker

faker = Faker()


@pytest.fixture(scope="session", autouse=False)
def auth_api_utils_unauthorized():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="session", autouse=False)
def auth_api_helper_unauthorized(auth_api_utils_unauthorized):
    api_helper = AuthorizationHelper(auth_api_utils_unauthorized)
    return api_helper


@pytest.fixture(scope="function", autouse=False)
def auth_api_service_unauthorized(auth_api_utils_unauthorized):
    auth_service = AuthService(api_utils=auth_api_utils_unauthorized)
    return auth_service


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_user(access_token_new_user):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL,
                         headers={f"Authorization": f"Bearer {access_token_new_user}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def access_token_new_user(auth_api_service_unauthorized):
    username = faker.user_name()
    email = faker.email()
    password = faker.password(
        length=30,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )

    auth_api_service_unauthorized.register_user(RegisterRequest(
        username=username,
        password=password,
        password_repeat=password,
        email=email
    ))

    login_response = auth_api_service_unauthorized.login_user(LoginRequest(
        username=username,
        password=password
    ))

    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def access_token_user(auth_api_service_unauthorized):
    load_dotenv()

    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    login_response = auth_api_service_unauthorized.login_user(LoginRequest(
        username=username,
        password=password
    ))

    return login_response.access_token


# @pytest.fixture(scope="session", autouse=True)
# def register_default_user(auth_api_helper_unauthorized):
#     load_dotenv()
#
#     username = os.getenv("API_USERNAME")
#     password = os.getenv("API_PASSWORD")
#
#     login_response = auth_api_helper_unauthorized.post_login(data=LoginRequest(
#         username=username,
#         password=password
#     ).model_dump())
#
#     if login_response.status_code == 401:
#         email = os.getenv("EMAIL")
#
#         auth_api_helper_unauthorized.post_register(RegisterRequest(
#             username=username,
#             password=password,
#             password_repeat=password,
#             email=email
#         ).model_dump())


@pytest.fixture(scope="function", autouse=False)
def university_service_user(university_api_utils_user):
    university_service = UniversityService(university_api_utils_user)
    return university_service


@pytest.fixture(scope="function", autouse=False)
def grade_helper_user(university_api_utils_user):
    helper = GradeHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="function", autouse=False)
def group_helper_user(university_api_utils_user):
    helper = GroupHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="function", autouse=False)
def student_helper_user(university_api_utils_user):
    helper = StudentHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="function", autouse=False)
def teacher_helper_user(university_api_utils_user):
    helper = TeacherHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="function", autouse=False)
def api_helper_unauthorized_invalid():
    helper = GroupHelper(
        ApiUtils(
            url=UniversityService.SERVICE_URL,
            headers={f"Authorization": f"Bearer {TokenData.INVALID_TOKEN}"}
        ))
    return helper
