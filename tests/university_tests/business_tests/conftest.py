import pytest

from services.university.university_service import UniversityService


@pytest.fixture(scope="function", autouse=False)
def university_service_user(university_api_utils_user):
    university_service = UniversityService(university_api_utils_user)
    return university_service
