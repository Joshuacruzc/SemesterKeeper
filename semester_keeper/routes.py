from flask import request, jsonify, render_template

from semester_keeper import app
from semester_keeper.models import db, Student, Course, StudentCourse, Curriculum, CourseCurriculum
from semester_keeper.schemas import course_schema, student_course_schema, student_courses_schema, student_schema, \
    curriculum_schema, course_curriculum_schema, courses_schema


# ---------------------------Test Routes ----------------------------------------
@app.route('/organize/<curriculum_id>', methods=['GET'])
def organize_curriculum(curriculum_id):
    curriculum = Curriculum.query.get(curriculum_id)
    curriculum.organize()
    # semesters = semesters_schema.dump(curriculum.semesters)
    semesters = curriculum.semesters
    semesters.sort(key=lambda x: x.position)
    return render_template('curriculum.html', semesters=curriculum.semesters)


# --------------------------HTML routes------------------------------------------
@app.route('/resources', methods=['GET'])
def resources():
    students = Student.query.all()
    courses = Course.query.all()
    curriculums = Curriculum.query.all()
    return render_template('resources.html', students=students, courses=courses, curriculums=curriculums)


@app.route('/profile/<student_id>')
def profile(student_id):
    student = Student.query.get(student_id)
    return render_template('profile.html', student=student)


# --------------------------API Endpoints----------------------------------------
@app.route('/student', methods=['POST'])
# Takes POST Request with student name and gpa keys defined in JSON
# Creates new student with specified name and GPA
# Returns created Student object in JSON
def add_student():
    name = request.json['name']
    gpa = request.json['gpa']
    curriculum = request.json['curriculum']
    student = Student(name=name, gpa=gpa, curriculum_id=curriculum)
    db.session.add(student)
    db.session.commit()
    student = student_schema.dump(student)
    return jsonify(student)


@app.route('/course', methods=['POST'])
# Takes POST Request with Course name and amount of credits defined in JSON
# Creates new course with specified name and amount of credits
# Returns created Course object as JSON
def add_course():
    name = request.json['name']
    credits = request.json['credits']
    course = Course(name=name, credits=credits)
    db.session.add(course)
    db.session.commit()
    course = course_schema.dump(course)
    return jsonify(course)


@app.route('/curriculum', methods=['POST'])
# Takes POST Request with curriculum name defined in JSON
# Creates new curriculum entity with specified name
# Returns Curriculum object as JSON
def add_curriculum():
    name = request.json['name']
    curriculum = Curriculum(name=name)
    db.session.add(curriculum)
    db.session.commit()
    curriculum = curriculum_schema.dump(curriculum)
    return jsonify(curriculum)


@app.route('/student_course', methods=['POST'])
# Takes POST Request with student_id, course_id and grade defined in JSON.
# Adds instance to many-to-many table between student and course
# Returns created instance of StudentCourse
def add_student_course():
    student_id = request.json['student_id']
    course_id = request.json['course_id']
    grade = request.json['grade']
    result = StudentCourse(student_id=student_id, course_id=course_id, grade=grade)
    db.session.add(result)
    db.session.commit()
    student_course = student_course_schema.dump(result)
    return jsonify(student_course)


@app.route('/course_curriculum', methods=['POST'])
# Takes POST Request with curriculum_id and course_id defined in JSON.
# Adds instance to many-to-many table between curriculum and course
# Returns created instance of CourseCurriculum
def add_course_to_curriculum():
    curriculun_id = request.json['curriculum_id']
    course_id = request.json['course_id']
    result = CourseCurriculum(curriculum_id=curriculun_id, course_id=course_id)
    db.session.add(result)
    db.session.commit()
    course_curriculum = course_curriculum_schema.dump(result)
    return jsonify(course_curriculum)


@app.route('/student/<student_id>', methods=['GET'])
# Takes GET Request with student_id defined in the URL
# Queries Student table to get student with specified student id
# Returns Student object as JSON
def get_student(student_id):
    student = Student.query.get(student_id)
    student = student_schema.dump(student)
    return jsonify(student)


@app.route('/student_courses/<student_id>', methods=['GET'])
# Takes GET Request with student_id defined in the URL
# Queries StudentCourse table to get all courses taken by this student
# Returns JSON with StudentCourse instances with specified student_id
def get_student_courses(student_id):
    student_courses = StudentCourse.query.filter_by(student_id=student_id)
    student_courses = student_courses_schema.dump(student_courses)
    return jsonify(student_courses)


@app.route('/remaining_courses/<student_id>', methods=['GET'])
# Takes GET Request with student_id defined in the URL
# Looks for courses taken by student and compares them with courses in Student Curriculum
# Returns JSON with Course instances
def get_remaining_courses(student_id):
    remaining_courses = []
    student = Student.query.get(student_id)
    taken_courses = student.courses
    curriculum_courses = student.curriculum.courses
    for course in curriculum_courses:
        if course not in taken_courses:
            remaining_courses.append(course.course)
    remaining_courses = courses_schema.dump(remaining_courses)
    return jsonify(remaining_courses)
