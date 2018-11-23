from marshmallow_sqlalchemy import ModelSchema

from semester_keeper.models import Student, Course, StudentCourse, Curriculum


class StudentSchema(ModelSchema):
    class Meta:
        model = Student
        fields = ('name', 'gpa', 'curriculum')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = ('name', 'credits')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


class CurriculumSchema(ModelSchema):
    class Meta:
        model = Curriculum
        fields = ('name', 'credits', 'courses')


curriculum_schema = CurriculumSchema()
curriculums_schema = CurriculumSchema(many=True)


class StudentCourseSchema(ModelSchema):
    class Meta:
        model = StudentCourse
        fields = ('course', 'grade')


student_course_schema = StudentCourseSchema()
student_courses_schema = StudentCourseSchema(many=True)
