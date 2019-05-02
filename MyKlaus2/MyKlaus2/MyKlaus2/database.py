from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from MyKlaus2 import app
engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    connect_args = {
        'port': int(app.config['SQLALCHEMY_DATABASE_PORT'])
    },
    echo='debug',
    echo_pool=True
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()

def init_db():
    import MyKlaus2.models
    import json
    import ntpath

    Base.metadata.create_all(engine)

    data = {}
    with open('data.txt') as json_file:  
        data = json.load(json_file)
    
    from MyKlaus2.models import Department, CourseOfStudy, Professor, Course, Exam, ExamType
    for department in data['DepAndCoS']:
        dep = Department(name=department)
        db_session.add(dep)
        db_session.commit()
        for courseofstudy in data['DepAndCoS'][department]:
            cos = CourseOfStudy(courseofstudy, dep)
            db_session.add(cos)
        db_session.commit()

    for professor in data['Prof']:
        prof = Professor(professor['lastname'], professor['firstname'])
        db_session.add(prof)
        db_session.commit()

    for course in data['Courses']:
        cour = Course(course)
        db_session.add(cour)
        db_session.commit()

    UnkProfs = {}

    for examtype in data['ExamAndTypes']:
        exTy = ExamType(examtype)
        db_session.add(exTy)
        db_session.commit()
        for exam in data['ExamAndTypes'][examtype]:
            filename = ntpath.basename(exam['filePath'])
            ex = Exam(exam['semester'], exam['year'], filename, exam['filePath'], exTy, db_session.query(Course).filter(Course.name == exam['Course']).first(), db_session.query(Department).filter(Department.idDepartment == exam['department']).first(), True)
            prof = db_session.query(Professor).filter(Professor.lastName == exam['docent']).first()
            if prof:
                prof.courses.append(ex.course)
            else:
                if ex.course.name not in UnkProfs:
                    UnkProfs[ex.course.name] = []
                if exam['docent'] not in UnkProfs[ex.course.name]:
                    UnkProfs[ex.course.name].append(exam['docent']) 
            db_session.add(ex)
        db_session.commit()

    with open('UnkCourseProfs.txt', 'w+', encoding='UTF-8') as json_file:
        json.dump(UnkProfs, json_file)

    print('Initialized the database.')
