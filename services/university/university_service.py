import random

from faker import Faker

from services.base_service import BaseService
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_student import DegreeEnumStr
from services.university.models.base_teacher import SubjectEnumStr
from services.university.models.grade_list_response import GradeListResponse
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse
from services.university.models.grade_statistic_response import GradeStatisticResponse
from services.university.models.group_list_response import GroupListResponse
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse

from utils.api_utils import ApiUtils


class UniversityService(BaseService):
    faker = Faker()

    SERVICE_URL = "http://localhost:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    """=================     GROUPS     ================="""

    def get_groups(self, ) -> GroupListResponse:
        response = self.group_helper.get_groups()
        return GroupListResponse(groups=response.json())

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponse(**response.json())

    def create_random_group(self):
        response = self.create_group(GroupRequest(name=f"{self.faker.word()}{random.randint(1, 100)}"))
        return response

    """=================     STUDENT     ================="""

    def create_student(self, student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_student(json=student_request.model_dump())
        return StudentResponse(**response.json())

    def create_random_student(self, group_id):
        response = self.create_student(
            StudentRequest(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                email=self.faker.email(),
                degree=random.choice(list(DegreeEnumStr)),
                phone="+" + self.faker.msisdn(),
                group_id=group_id
            ))

        return response

    """=================     TEACHER     ================="""

    def create_teacher(self, teacher_request: TeacherRequest) -> TeacherResponse:
        response = self.teacher_helper.post_teacher(json=teacher_request.model_dump())
        return TeacherResponse(**response.json())

    def create_random_teacher(self):
        response = self.create_teacher(
            TeacherRequest(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                subject=random.choice(list(SubjectEnumStr))
            ))

        return response

    """=================     GRADES     ================="""

    def get_grades(self, params: dict = None) -> GradeListResponse:
        response = self.grade_helper.get_grades(params=params)
        return GradeListResponse(grades=response.json())

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grade(data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def get_grade_stats(self, params: dict = None) -> GradeStatisticResponse:
        response = self.grade_helper.get_grade_stats(params=params)
        return GradeStatisticResponse(**response.json())

    def get_count_grade(self, params: dict = None) -> int:
        response = self.grade_helper.get_grades(params=params)
        return len(GradeListResponse(grades=response.json()).grades)

    def get_max_grade(self, params: dict = None) -> int:
        response = self.grade_helper.get_grades(params=params)
        return max(GradeResponse(**g).grade for g in response.json())

    def get_min_grade(self, params: dict = None) -> int:
        response = self.grade_helper.get_grades(params=params)
        return min(GradeResponse(**g).grade for g in response.json())

    def get_avg_grade(self, params: dict = None) -> float:
        response = self.grade_helper.get_grades(params=params)
        count_grade = self.get_count_grade(params)

        if count_grade > 1:
            avg = sum(GradeResponse(**g).grade for g in response.json()) / count_grade
        else:
            avg = None

        return avg
