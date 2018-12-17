from semester_keeper import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    credits = db.Column(db.Integer)

    def __repr__(self):
        return f"Course: {self.name}"


class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    credits = db.Column(db.Integer, default=0)
    courses = db.relationship("CourseCurriculum", back_populates="curriculum")

    def __repr__(self):
        return f"Curriculum: {self.name}"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    gpa = db.Column(db.Float)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey('curriculum.id'), nullable=True)
    curriculum = db.relationship(Curriculum, backref=db.backref("students"))
    courses = db.relationship("StudentCourse", back_populates="student")

    def __repr__(self):
        return f"Student: {self.name}"


class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    student = db.relationship(Student, back_populates="courses")
    course = db.relationship(Course, backref=db.backref("students"))
    grade = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.student}, {self.course}"


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey("curriculum.id"), nullable=False)
    curriculum = db.relationship(Curriculum, backref=db.backref("semesters"))
    credits = db.Column(db.Integer, default=0)


class CourseCurriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey("curriculum.id"), nullable=False)
    course_id = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)
    curriculum = db.relationship(Curriculum, back_populates="courses")
    course = db.relationship(Course, backref=db.backref("curriculum_assoc"))
    semester_id = db.Column('semester_id', db.Integer, db.ForeignKey('semester.id'), nullable=True)
    semester = db.relationship(Semester, backref=db.backref("courses"))

    def __init__(self, *args, **kwargs):
        super(CourseCurriculum, self).__init__(*args, **kwargs)
        self.curriculum.credits += self.course.credits

    def __repr__(self):
        return f"{self.curriculum}, {self.course}"


class PreReqCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prerequisite_id = db.Column('prereq_id', db.Integer, db.ForeignKey("course_curriculum.id"), nullable=False)
    unlocked_id = db.Column('unlocked_id', db.Integer, db.ForeignKey("course_curriculum.id"), nullable=False)
    prerequisite = db.relationship(CourseCurriculum, foreign_keys=[prerequisite_id], backref=db.backref("unlocked_courses"))
    unlocked = db.relationship(CourseCurriculum, foreign_keys=[unlocked_id], backref=db.backref("prerequisites"))
