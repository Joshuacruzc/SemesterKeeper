from semester_keeper import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    credits = db.Column(db.Integer)


class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    credits = db.Column(db.Integer)
    courses = db.relationship("CourseCurriculum", back_populates="curriculum")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    gpa = db.Column(db.Float)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey('curriculum.id'), nullable=True)
    curriculum = db.relationship(Curriculum, backref=db.backref("students"))
    courses = db.relationship("StudentCourse", back_populates="student")


class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    student = db.relationship(Student, back_populates="courses")
    course = db.relationship(Course, backref=db.backref("students"))
    grade = db.Column(db.Integer)


class CourseCurriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey("curriculum.id"), nullable=False)
    course_id = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)
    curriculum = db.relationship(Curriculum, back_populates="courses")
    course = db.relationship(Course, backref=db.backref("curriculum_assoc"))
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
