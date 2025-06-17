import random

import pytest
from faker import Faker

from services.university.models.grade_request import GradeRequest


class TestBusinessU:
    faker = Faker()

    def test_create_grade(self, university_service_user):
        group_id = university_service_user.create_random_group().id
        teacher_id = university_service_user.create_random_teacher().id
        student_id = university_service_user.create_random_student(group_id).id

        id_grade = university_service_user.create_grade(
            GradeRequest(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=random.randint(1, 5)
            )).id

        query_param = {"teacher_id": teacher_id, "group_id": group_id, "student_id": student_id}
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

        random_response = random.choice(grade_list.grades)
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

        random_response = random.choice(grade_list.grades)
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
