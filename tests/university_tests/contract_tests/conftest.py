import pytest

from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper


@pytest.fixture(scope="session", autouse=False)
def grade_helper_user(university_api_utils_user):
    helper = GradeHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="session", autouse=False)
def group_helper_user(university_api_utils_user):
    helper = GroupHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="session", autouse=False)
def student_helper_user(university_api_utils_user):
    helper = StudentHelper(university_api_utils_user)
    return helper


@pytest.fixture(scope="session", autouse=False)
def teacher_helper_user(university_api_utils_user):
    helper = TeacherHelper(university_api_utils_user)
    return helper
