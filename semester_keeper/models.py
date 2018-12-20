from semester_keeper import db


class Course(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    department = db.Column(db.String(4))
    course_num = db.Column(db.String(4))
    # name = db.Column(db.String(120))
    credits = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.id = kwargs['department'] + kwargs['course_num']
        super(Course, self).__init__(**kwargs)

    def __repr__(self):
        return f"Course: {self.name}"


class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    credits = db.Column(db.Integer, default=0)
    courses = db.relationship("CourseCurriculum", back_populates="curriculum")
    max_semester_credits = db.Column(db.Integer, default=16)

    def __repr__(self):
        return f"Curriculum: {self.name}"

    def get_department_paths(self):
        departments = []
        query = CourseCurriculum.query.filter_by(curriculum=self).join(Course)
        for course in query.distinct('department'):
            path = query.filter_by(department=course.course.department)
            count = path.distinct('level').count()
            path = path.order_by('level')
            departments.append((path, count))
        departments.sort(key=lambda tup: tup[1])
        departments.reverse()
        return departments

    def organize(self):
        paths = self.get_department_paths()
        for path in paths:
            for course in path[0]:
                available_semesters = course.curriculum.semesters
                semester_position = course.get_soonest_semester()

                for position in range(semester_position, len(available_semesters)):
                    if course.course.credits <= available_semesters[position].free_space:
                        available_semesters[position].add_course(course)
                        break
                    semester_position += 1
                if not course.semester:
                    semester = Semester(position=semester_position, curriculum=course.curriculum)
                    db.session.add(semester)
                    db.session.commit()
                    semester.add_course(course)
        db.session.commit()


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
    course_id = db.Column(db.String(8), db.ForeignKey("course.id"), nullable=False)
    student = db.relationship(Student, back_populates="courses")
    course = db.relationship(Course, backref=db.backref("students"))
    grade = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.student}, {self.course}"


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey("curriculum.id"), nullable=False)
    curriculum = db.relationship(Curriculum, backref=db.backref("semesters"))
    credits = db.Column(db.Integer, default=0)
    free_space = db.Column(db.Integer)
    courses = db.relationship("CourseCurriculum", back_populates="semester")

    def __init__(self, *args, **kwargs):
        super(Semester, self).__init__(*args, **kwargs)
        self.free_space = self.curriculum.max_semester_credits

    def add_course(self, course):
        self.courses.append(course)
        self.credits += course.course.credits
        self.free_space = self.curriculum.max_semester_credits - self.credits


class CourseCurriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curriculum_id = db.Column('curriculum_id', db.Integer, db.ForeignKey("curriculum.id"), nullable=False)
    course_id = db.Column('course_id', db.String(8), db.ForeignKey("course.id"), nullable=False)
    curriculum = db.relationship(Curriculum, back_populates="courses")
    course = db.relationship(Course, backref=db.backref("curriculum_assoc"))
    semester_id = db.Column('semester_id', db.Integer, db.ForeignKey('semester.id'), nullable=True)
    semester = db.relationship(Semester, back_populates="courses")
    level = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(CourseCurriculum, self).__init__(*args, **kwargs)
        self.curriculum.credits += self.course.credits

    def get_soonest_semester(self):
        position = self.level
        for course in self.prerequisite:
            if course.prerequisite.semester:
                position = max(position, course.prerequisite.semester.position + 1)
        return position

    def __repr__(self):
        return f"{self.curriculum}, {self.course}"


class PreReqCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prerequisite_id = db.Column('prereq_id', db.Integer, db.ForeignKey("course_curriculum.id"), nullable=False)
    unlocked_id = db.Column('unlocked_id', db.Integer, db.ForeignKey("course_curriculum.id"), nullable=False)
    prerequisite = db.relationship(CourseCurriculum, foreign_keys=[prerequisite_id], backref=db.backref("unlocked"))
    unlocked = db.relationship(CourseCurriculum, foreign_keys=[unlocked_id], backref=db.backref("prerequisite"))

    def __init__(self, *args, **kwargs):
        super(PreReqCourse, self).__init__(*args, **kwargs)
        self.unlocked.level = max(self.unlocked.level, self.prerequisite.level + 1)
