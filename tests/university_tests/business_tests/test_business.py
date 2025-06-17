from random import randint, choice

import pytest
from faker import Faker

from services.university.models.conflict_response import ConflictResponse
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest


class TestBusinessU:
    faker = Faker()

    def test_create_grade(self, university_service_user):
        group_id = university_service_user.create_random_group().id
        teacher_id = university_service_user.create_random_teacher().id
        student_id = university_service_user.create_random_student(group_id).id

        grade_response = university_service_user.create_grade(
            GradeRequest(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=randint(1, 5)
            ))

        id_grade = grade_response.id
        query_param = grade_response.model_dump()

        grade_list = university_service_user.get_grades(query_param)

        assert id_grade in [grade.id for grade in grade_list.grades], \
            f"Expected grade ID: {id_grade} in grade list, but was not found"

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
        "student_id"
        # "group_id" у бэека нет такого параметра в ответе
    ])
    def test_grade_list_filtered(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        expected_param = getattr(random_response, filter_name)

        filtered_list = university_service_user.get_grades({filter_name: expected_param})

        assert random_response in filtered_list.grades, \
            f"Expected obj: {random_response}, but got: {filtered_list}"

        for obj in filtered_list.grades:
            actual_param = getattr(obj, filter_name)

            assert expected_param == actual_param, \
                f"Expected only {expected_param} for filter: {filter_name} in response, but got {actual_param}"

    @pytest.mark.parametrize("filter_name", [
        "teacher_id",
        "student_id"
        # "group_id" у бэка нет такого параметра в ответе
    ])
    def test_grade_stats_filtered(self, university_service_user, filter_name):
        grade_list = university_service_user.get_grades()

        random_response = choice(grade_list.grades)
        filter_value = getattr(random_response, filter_name)

        request_param = {filter_name: filter_value}

        expected_count_grades = university_service_user.get_count_grade(request_param)
        expected_max_grade = university_service_user.get_max_grade(request_param)
        expected_min_grade = university_service_user.get_min_grade(request_param)
        expected_avg_grade = university_service_user.get_avg_grade(request_param)

        stats_list = university_service_user.get_grade_stats(request_param)

        assert expected_count_grades == stats_list.count, f"Expected {expected_count_grades}, but got {stats_list.count}"
        assert expected_max_grade == stats_list.max, f"Expected {expected_max_grade}, but got {stats_list.max}"
        assert expected_min_grade == stats_list.min, f"Expected {expected_min_grade}, but got {stats_list.min}"
        assert expected_avg_grade == stats_list.avg, f"Expected {expected_avg_grade}, but got {stats_list.avg}"

    def test_create_group_not_authorized(self):
        pass

    def test_create_group_forbidden(self):
        pass

    def test_create_group_conflict(self, university_service_user, university_helper_user):
        groups_response_list = university_service_user.get_groups()
        existing_group_name = choice(groups_response_list.groups).name

        json = GroupRequest(name=existing_group_name).model_dump()
        group_response = university_helper_user.group.post_group(json=json)

        conflict_response = ConflictResponse(**group_response.json())
        assert conflict_response.detail == "Group is already created"


    def test_create_group_validation_error(self):
        pass