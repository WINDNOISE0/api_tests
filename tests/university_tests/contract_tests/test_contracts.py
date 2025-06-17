from random import randint, choice

import pytest
from faker import Faker

from services.university.helpers.group_helper import GroupHelper
from services.university.models.base_student import DegreeEnumStr
from services.university.models.base_teacher import SubjectEnumStr
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils


class TestContracts:
    faker = Faker()

    def test_group_create_201(self, university_helper_user):
        json = GroupRequest(name=f"{self.faker.word()}{randint(1, 100)}").model_dump()
        group_response = university_helper_user.group.post_group(json=json)

        assert 201 == group_response.status_code, f"Expected status code:{201}, but got {group_response.status_code}"

    def test_teacher_create_201(self, university_helper_user):
        json = TeacherRequest(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            subject=choice(list(SubjectEnumStr))
        ).model_dump()

        teacher_response = university_helper_user.teacher.post_teacher(json=json)
        assert 201 == teacher_response.status_code, f"Expected status code:{201}, but got {teacher_response.status_code}"

    def test_student_create_201(self, university_helper_user, university_service_user):
        group_id = university_service_user.create_random_group().id

        json = StudentRequest(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            email=self.faker.email(),
            degree=choice(list(DegreeEnumStr)),
            phone="+" + self.faker.msisdn(),
            group_id=group_id
        ).model_dump()

        student_response = university_helper_user.student.post_student(json=json)
        assert 201 == student_response.status_code, f"Expected status code:{201}, but got {student_response.status_code}"

    def test_grades_create_201(self, university_helper_user, university_service_user):
        group_id = university_service_user.create_random_group().id
        teacher_id = university_service_user.create_random_teacher().id
        student_id = university_service_user.create_random_student(group_id).id

        data = GradeRequest(
            teacher_id=teacher_id,
            student_id=student_id,
            grade=randint(1, 5)
        ).model_dump()

        grade_response = university_helper_user.grade.post_grade(data=data)

        assert 201 == grade_response.status_code, f"Expected status code:{201}, but got {grade_response.status_code}"

    def test_group_create_409(self, university_helper_user, university_service_user):
        groups_response_list = university_service_user.get_groups()
        existing_group_name = choice(groups_response_list.groups).name

        json = GroupRequest(name=existing_group_name).model_dump()
        group_response = university_helper_user.group.post_group(json=json)

        assert 409 == group_response.status_code, f"Expected status code:{409}, but got {group_response.status_code}"

    @pytest.mark.parametrize("value", [
        12342,
        True,
        None
    ])
    def test_group_create_422(self, value, university_helper_user):
        json = {"name": value}

        group_response = university_helper_user.group.post_group(json=json)

        assert 422 == group_response.status_code, f"Expected status code:{422}, but got {group_response.status_code}"

    def test_group_create_403(self, auth_api_utils_unauthorized):
        api_helper_unauthorized = GroupHelper(ApiUtils(url=UniversityService.SERVICE_URL))
        json = GroupRequest(name=f"{self.faker.word()}{randint(1, 100)}").model_dump()

        group_response = api_helper_unauthorized.post_group(json=json)

        assert 403 == group_response.status_code, f"Expected status code:{403}, but got {group_response.status_code}"

    def test_group_create_401(self):
        invalid_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiQWxleFRlc3QiLCJleHAiOjE3NTAxOTgyNzIsImlhdCI6MTc1MDE5MTA3Mn0.HtF7wLoMhE84p8o2wtoRyzsYeXNUy5MCWRXQr3SYxkzLdkqKtYCM0-ooA6By4HFESGcLpqTCKoBJI27XBhZtk0NIwawprkDjWaEgdNao6fiWc-eIF9gmqOI1WhloXrvesLQsPKGvrWLzTjLjW-0patzLAF1JCLKcjMjfiPMm9fldcLtsjlLxTOGXSZbKUVyRlyTZBFg501p83K3DDik3agycXyiSMnNxcI9ETbooPR2nOMbVjlqLha9YlwQALw1Wi_1RGN0gYMoSXDdTKSVTiTA5JzuljsD7XYR-EPIP6prg6wUA7kfs0_8SeFmI4UvjmeHP_oLezWw-2FwnmQ4UNw"
        api_helper_unauthorized = GroupHelper(
            ApiUtils(url=UniversityService.SERVICE_URL, headers={f"Authorization": f"Bearer {invalid_token}"}))
        json = GroupRequest(name=f"{self.faker.word()}{randint(1, 100)}").model_dump()

        group_response = api_helper_unauthorized.post_group(json=json)

        assert 401 == group_response.status_code, f"Expected status code:{401}, but got {group_response.status_code}"
