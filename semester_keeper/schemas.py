from marshmallow_sqlalchemy import ModelSchema

from semester_keeper.models import Student, Course, StudentCourse


class StudentSchema(ModelSchema):
    class Meta:
        model = Student
        fields = ('name', 'gpa')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = ('name', 'credits')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


class StudentCourseSchema(ModelSchema):
    class Meta:
        model = StudentCourse
        fields = ('course', 'grade')


student_course_schema = StudentCourseSchema()
student_courses_schema = StudentCourseSchema(many=True)
