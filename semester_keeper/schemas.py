from marshmallow.fields import Nested
from marshmallow_sqlalchemy import ModelSchema

from semester_keeper.models import Student, Course, StudentCourse, Curriculum, CourseCurriculum


class CourseSchema(ModelSchema):
    class Meta:
        model = Course


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


class CurriculumSchema(ModelSchema):
    courses = Nested(CourseSchema)

    class Meta:
        model = Curriculum


curriculum_schema = CurriculumSchema()
curriculums_schema = CurriculumSchema(many=True)


class StudentSchema(ModelSchema):
    curriculum = Nested(CurriculumSchema)
    courses = Nested(CourseSchema)

    class Meta:
        model = Student


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class StudentCourseSchema(ModelSchema):
    course = Nested(CourseSchema)
    student = Nested(StudentSchema)

    class Meta:
        model = StudentCourse


student_course_schema = StudentCourseSchema()
student_courses_schema = StudentCourseSchema(many=True)


class CourseCurriculumSchema(ModelSchema):
    course = Nested(CourseSchema)
    curriculum = Nested(CurriculumSchema)

    class Meta:
        model = CourseCurriculum


course_curriculum_schema = CourseCurriculumSchema()
course_curriculums_schema = CourseCurriculumSchema(many=True)