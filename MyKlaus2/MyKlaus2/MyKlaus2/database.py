from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from MyKlaus2 import app
engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    connect_args = {
        'port': int(app.config['SQLALCHEMY_DATABASE_PORT'])
    },
    echo=False,
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
    from sqlalchemy import or_

    Base.metadata.create_all(engine)

    data = {}
    with open('data.txt') as json_file:  
        data = json.load(json_file)

    from MyKlaus2.models import Department, Professor, Course, Exam, ExamType
    for department in data['Dep']:
        db_session.add(Department(name=data['Dep'][department]))
        db_session.commit()

    UnkProf = Professor("Unbekannt");
    db_session.add(UnkProf)
    db_session.commit()
    for professor in data['Prof']:
        db_session.add(Professor(professor['lastname'], professor['firstname']))
        db_session.commit()

    for idCourse in data['Courses']:
        db_session.add(Course(data['Courses'][idCourse]['name'], db_session.query(Department).filter(Department.name == data['Courses'][idCourse]['dep']).first()))
        db_session.commit()

    for examtype in data['ExamAndTypes']:
        exTy = ExamType(examtype)
        db_session.add(exTy)
        db_session.commit()
        for exam in data['ExamAndTypes'][examtype]:

            sem = exam['semester']
            year = exam['year']
            fname = ntpath.basename(exam['filePath'])
            fpath = exam['filePath']
            cour = db_session.query(Course).filter(Course.name == exam['Course']).first()
            dep = db_session.query(Department).filter(Department.name == exam['department']).first()
            docent = exam['docent']
            prof = db_session.query(Professor).filter(or_(Professor.firstName == docent, Professor.lastName == docent)).first()
            
            if not prof:
                docent.split(" ")
                for x in docent:
                    prof = db_session.query(Professor).filter(or_(Professor.firstName == x, Professor.lastName == x)).first()
            
            if not prof:
                docent.split("/")
                for x in docent:
                    prof = db_session.query(Professor).filter(or_(Professor.firstName == x, Professor.lastName == x)).first()
            
            if not prof:
                docent.split("\\")
                for x in docent:
                    prof = db_session.query(Professor).filter(or_(Professor.firstName == x, Professor.lastName == x)).first()
            
            if not prof:
                prof = UnkProf
            
            ex = Exam(sem, year, fname, fpath, cour, dep, exTy, prof, True)
            db_session.add(ex)
            db_session.commit()

    print('Initialized the database.')
