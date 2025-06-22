from random import randint, choice

import pytest
from faker import Faker

from services.university.helpers.group_helper import GroupHelper
from services.university.models.student.base_student import DegreeEnumStr
from services.university.models.teacher.base_teacher import SubjectEnumStr
from services.university.models.grade.grade_request import GradeRequest
from services.university.models.group.group_request import GroupRequest
from services.university.models.student.student_request import StudentRequest
from services.university.models.teacher.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from test_data.token_data import TokenData
from utils.api_utils import ApiUtils


class TestContracts:
    faker = Faker()
    MIN_GRADE = 1
    MAX_GRADE = 5
    RANDOM_NAME = f"{faker.word()}{randint(1, 100)}"

    def test_group_create_201(self, group_helper_user):
        json = GroupRequest(name=self.RANDOM_NAME).model_dump()
        group_response = group_helper_user.post_group(json=json)

        assert 201 == group_response.status_code, f"Expected status code:{201}, but got {group_response.status_code}"

    def test_teacher_create_201(self, teacher_helper_user):
        json = TeacherRequest(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            subject=choice(list(SubjectEnumStr))
        ).model_dump()

        teacher_response = teacher_helper_user.post_teacher(json=json)
        assert 201 == teacher_response.status_code, f"Expected status code:{201}, but got {teacher_response.status_code}"

    def test_student_create_201(self, student_helper_user, university_service_user):
        group_id = university_service_user.create_random_group().id

        json = StudentRequest(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            email=self.faker.email(),
            degree=choice(list(DegreeEnumStr)),
            phone="+" + self.faker.msisdn(),
            group_id=group_id
        ).model_dump()

        student_response = student_helper_user.post_student(json=json)
        assert 201 == student_response.status_code, f"Expected status code:{201}, but got {student_response.status_code}"

    def test_grades_create_201(self, grade_helper_user, university_service_user):
        group_id = university_service_user.create_random_group().id
        teacher_id = university_service_user.create_random_teacher().id
        student_id = university_service_user.create_random_student(group_id).id

        data = GradeRequest(
            teacher_id=teacher_id,
            student_id=student_id,
            grade=randint(self.MIN_GRADE, self.MAX_GRADE)
        ).model_dump()

        grade_response = grade_helper_user.post_grade(data=data)

        assert 201 == grade_response.status_code, f"Expected status code:{201}, but got {grade_response.status_code}"

    def test_group_create_409(self, group_helper_user, university_service_user):
        groups_response_list = university_service_user.get_groups()
        existing_group_name = choice(groups_response_list.groups).name

        json = GroupRequest(name=existing_group_name).model_dump()
        group_response = group_helper_user.post_group(json=json)

        assert 409 == group_response.status_code, f"Expected status code:{409}, but got {group_response.status_code}"

    @pytest.mark.parametrize("value", [
        12342,
        True,
        None
    ])
    def test_group_create_422(self, value, group_helper_user):
        json = {"name": value}

        group_response = group_helper_user.post_group(json=json)

        assert 422 == group_response.status_code, f"Expected status code:{422}, but got {group_response.status_code}"

    def test_group_create_403(self, auth_api_utils_unauthorized):
        api_helper_unauthorized = GroupHelper(ApiUtils(url=UniversityService.SERVICE_URL))
        json = GroupRequest(name=self.RANDOM_NAME).model_dump()

        group_response = api_helper_unauthorized.post_group(json=json)

        assert 403 == group_response.status_code, f"Expected status code:{403}, but got {group_response.status_code}"

    def test_group_create_401(self):
        api_helper_unauthorized = GroupHelper(
            ApiUtils(
                url=UniversityService.SERVICE_URL,
                headers={f"Authorization": f"Bearer {TokenData.INVALID_TOKEN}"}
            ))

        json = GroupRequest(name=self.RANDOM_NAME).model_dump()

        group_response = api_helper_unauthorized.post_group(json=json)

        assert 401 == group_response.status_code, f"Expected status code:{401}, but got {group_response.status_code}"
