from semester_keeper import db
from semester_keeper.models import Curriculum, Course, CourseCurriculum, PreReqCourse


def import_curriculum(name):
    file = open(name + '.txt', 'r')
    curriculum = Curriculum(name=name)
    db.session.add(curriculum)
    db.session.commit()
    for line in file:
        line = line.split()
        print(line)
        course = Course(department=line[0][:4], course_num=line[0][4:], credits=int(line[1]))
        db.session.add(course)
        course_curriculum = CourseCurriculum(curriculum=curriculum, course=course)
        db.session.add(course_curriculum)
        # if line[2] != '--------':
        #     courses = line[2].split(',')
        #     for correq in courses:
        #         course.correquisites.append((Course.query.filter_by(name=correq))
        if line[3] != '--------':
            courses = line[3].split(',')
            for prereq in courses:
                prerequisite = CourseCurriculum.query.filter_by(curriculum=curriculum,
                                                                course=Course.query.get(prereq)).first()
                prereq = PreReqCourse(prerequisite=prerequisite,
                             unlocked=course_curriculum)
                db.session.add(prereq)

    db.session.commit()


import_curriculum('CIIC')
