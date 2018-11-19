from semester_keeper import db


class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column('student_id', db.Integer, db.ForeignKey("student.id"), nullable=False)
    course = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)
    grade = db.Column(db.Integer)

    def __init__(self, student, course, grade):
        self.student = student
        self.course = course
        self.grade = grade


class CourseCurriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curriculum = db.Column('curriculum_id', db.Integer, db.ForeignKey("curriculum.id"), nullable=False)
    course = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)
    semester = db.Column(db.Integer)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    gpa = db.Column(db.Float)
    courses = db.relationship('Course', backref='Students', secondary='student_course', cascade='all')

    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    credits = db.Column(db.Integer)

    def __init__(self, name, credits):
        self.name = name
        self.credits = credits


class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    courses = db.relationship('Course', backref='Curriculums', secondary='course_curriculum', cascade='all')