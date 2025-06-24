from random import randint, choice

import pytest
from faker import Faker
from pytest_check import check

from services.university.helpers.group_helper import GroupHelper
from services.university.models.error.error import Error, ErrorText
from services.university.models.error.validation_error_list import ValidationErrorList
from services.university.models.grade.grade_base import MIN_GRADE, MAX_GRADE
from services.university.models.grade.grade_request import GradeRequest
from services.university.models.group.group_request import GroupRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils


class TestBusinessU:
    faker = Faker()
    RANDOM_NAME = f"{faker.word()}{randint(1, 100)}"

    def test_create_grade(self, university_service_user):
        group_id = university_service_user.create_random_group().id
        teacher_id = university_service_user.create_random_teacher().id
        student_id = university_service_user.create_random_student(group_id).id

        grade_response = university_service_user.create_grade(
            GradeRequest(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=randint(MIN_GRADE, MAX_GRADE)
            ))

        id_grade = grade_response.id
        query_param = grade_response.model_dump()

        grade_list = university_service_user.get_grades(query_param)

        assert id_grade in [grade.id for grade in grade_list.grades], \
            f"Expected grade ID: {id_grade} in grade list, but was not found"

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
        "student_id"
    ])
    def test_grade_list_filtered(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        expected_param = getattr(random_response, filter_name)

        filtered_list = university_service_user.get_grades({filter_name: expected_param})

        check.is_in(random_response, filtered_list.grades, f"Expected obj: {random_response}, but got: {filtered_list.grades}")

        for obj in filtered_list.grades:
            actual_param = getattr(obj, filter_name)

            check.equal(expected_param, actual_param,
                        f"Expected only {expected_param} for filter: {filter_name} in response, but got {actual_param}")

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
        "student_id"
        # "group_id" у бэка нет такого параметра в ответе
    ])
    def test_filtered_grade_count(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        filter_value = getattr(random_response, filter_name)

        request_param = {filter_name: filter_value}

        expected_count_grades = university_service_user.get_count_grade(request_param)
        stats_list = university_service_user.get_grade_stats(request_param)

        assert expected_count_grades == stats_list.count, f"Expected {expected_count_grades}, but got {stats_list.count}"

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
    ])
    def test_filtered_grade_max(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        filter_value = getattr(random_response, filter_name)

        request_param = {filter_name: filter_value}

        expected_max_grade = university_service_user.get_max_grade(request_param)
        stats_list = university_service_user.get_grade_stats(request_param)

        assert expected_max_grade == stats_list.max, f"Expected {expected_max_grade}, but got {stats_list.max}"

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
        "student_id"
    ])
    def test_filtered_grade_min(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        filter_value = getattr(random_response, filter_name)

        request_param = {filter_name: filter_value}

        expected_min_grade = university_service_user.get_min_grade(request_param)
        stats_list = university_service_user.get_grade_stats(request_param)

        assert expected_min_grade == stats_list.min, f"Expected {expected_min_grade}, but got {stats_list.min}"

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
        "student_id"
    ])
    def test_filtered_grade_avg(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        filter_value = getattr(random_response, filter_name)

        request_param = {filter_name: filter_value}

        expected_avg_grade = university_service_user.get_avg_grade(request_param)
        stats_list = university_service_user.get_grade_stats(request_param)

        assert expected_avg_grade == stats_list.avg, f"Expected {expected_avg_grade}, but got {stats_list.avg}"

    def test_create_group_no_auth(self):
        api_helper_unauthorized = GroupHelper(ApiUtils(url=UniversityService.SERVICE_URL))
        json = GroupRequest(name=self.RANDOM_NAME).model_dump()

        group_response = api_helper_unauthorized.post_group(json=json)

        no_authorized_response = Error(**group_response.json())
        assert ErrorText.NO_AUTH == no_authorized_response.detail, f"Expected error text: {ErrorText.NO_AUTH}, but got {no_authorized_response.detail}"

    def test_create_group_forbidden(self, api_helper_unauthorized_invalid):
        json = GroupRequest(name=self.RANDOM_NAME).model_dump()

        group_response = api_helper_unauthorized_invalid.post_group(json=json)
        forbidden_response = Error(**group_response.json())

        assert ErrorText.FORBIDDEN == forbidden_response.detail, f"Expected error text: {ErrorText.FORBIDDEN}, but got {forbidden_response.detail}"

    def test_create_group_conflict(self, university_service_user, group_helper_user):
        groups_response_list = university_service_user.get_groups()
        existing_group_name = choice(groups_response_list.groups).name

        json = GroupRequest(name=existing_group_name).model_dump()
        group_response = group_helper_user.post_group(json=json)

        conflict_response = Error(**group_response.json())
        assert ErrorText.CONFLICT_RESPONSE == conflict_response.detail, f"Expected error text: {ErrorText.CONFLICT_RESPONSE}, but got {conflict_response.detail}"

    @pytest.mark.parametrize("value", [
        12342,
        True,
        None
    ])
    def test_create_group_validation_error(self, value, group_helper_user):
        json = {"name": value}

        group_response = group_helper_user.post_group(json=json)

        validation_error_response = ValidationErrorList(**group_response.json())

        assert validation_error_response.detail, "detail field should not be empty"
