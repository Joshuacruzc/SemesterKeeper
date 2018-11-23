from flask import request, jsonify

from semester_keeper import app
from semester_keeper.models import db, Student, Course, StudentCourse, Curriculum
from semester_keeper.schemas import course_schema, student_course_schema, student_courses_schema, student_schema, \
    curriculum_schema


@app.route('/student', methods=['POST'])
# Takes POST Request with student name and gpa keys defined in JSON
# Creates new student with specified name and GPA
# Returns created Student object in JSON
def add_student():
    name = request.json['name']
    gpa = request.json['gpa']
    curriculum = request.json['curriculum']
    student = Student(name, gpa, curriculum)
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
    course = Course(name, credits)
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
    curriculum = Curriculum(name)
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
    result = StudentCourse(student=student_id, course=course_id, grade=grade)
    db.session.add(result)
    db.session.commit()
    student_course = student_course_schema.dump(result)
    return jsonify(student_course)


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
    student_courses = StudentCourse.query.filter_by(student=student_id)
    student_courses = student_courses_schema.dump(student_courses)
    return jsonify(student_courses)