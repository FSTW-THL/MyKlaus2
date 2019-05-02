from sqlalchemy import Table, Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from MyKlaus2.database import Base
import enum

#Enums
class SemesterEnum(enum.Enum):
    SS = 'SS'
    WS = 'WS'

#Assoziations Tabellen
CourseOfStudy_has_Course = Table('CourseOfStudy_has_Course', Base.metadata,
    Column('CourseOfStudy_idCourseOfStudy', Integer, ForeignKey('CourseOfStudy.idCourseOfStudy'), nullable=False),
    Column('Course_idCourse', Integer, ForeignKey('Course.idCourse'), nullable=False)
)

Course_has_Professor = Table('Course_has_Professor', Base.metadata,
    Column('Course_idCourse', Integer, ForeignKey('Course.idCourse'), nullable=False),
    Column('Professor_idProfessor', Integer, ForeignKey('Professor.idProfessor'), nullable=False)
)

#Tabellen
class Department(Base):
    __tablename__ = 'Department'

    idDepartment = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    coursesOfStudy = relationship('CourseOfStudy', back_populates='department', lazy=True, order_by='CourseOfStudy.name')
    exams = relationship('Exam', back_populates='department', lazy=True, order_by='desc(Exam.year)')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Department(idDepartment=%d, name="%s">' % (self.idDepartment, self.name)

    def to_dict(self):
        return {
            'idDepartment': self.idDepartment,
            'name': self.name,
            'coursesOfStudy': self.coursesOfStudy,
            'exams': self.exams
        }

class CourseOfStudy(Base):
    __tablename__ = 'CourseOfStudy'

    idCourseOfStudy = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    Department_idDepartment = Column(Integer, ForeignKey('Department.idDepartment'), nullable=False)
    department = relationship("Department", back_populates='coursesOfStudy', uselist=False)

    courses = relationship("Course", secondary=CourseOfStudy_has_Course, back_populates="coursesOfStudy")

    def __init__(self, name, department):
        self.name = name
        self.Department_idDepartment = department.idDepartment

    def __repr__(self):
        return '<CourseOfStudy(idCourseOfStudy=%d, name="%s", department=%s)>' % (self.idCouseOfStudy, self.name, self.depadepartment)

    def to_dict(self):
        return {
            'idCourseOfStudy': self.idCourseOfStudy,
            'name': self.name,
            'department': self.department,
            'courses': self.courses
        }

class Professor(Base):
    __tablename__ = 'Professor'

    idProfessor = Column(Integer, primary_key=True)
    firstName = Column(String(128))
    lastName = Column(String(128), nullable=False)
    isAgainstMyKlaus = Column(Boolean, nullable=False, default=True)
    courses = relationship("Course", secondary=Course_has_Professor, back_populates="professors")

    def __init__(self, lastName, firstName=None, isAgainstMyKlaus=True):
        self.firstName = firstName
        self.lastName = lastName
        self.isAgainstMyKlaus = isAgainstMyKlaus

    def __repr__(self):
        return '<Professor(idProfessor=%d, firstName="%s", lastName="%s", isAgainstMyKlaus=%d)>' % (self.idProfessor, self.firstName, self.lastName, self.isAgainstMyKlaus)

    def to_dict(self):
        return {
            'idProfessor': self.idProfessor,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'isAgainstMyKlaus': self.isAgainstMyKlaus,
            'courses': self.courses
        }

class Course(Base):
    __tablename__ = 'Course'

    idCourse = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    exams = relationship('Exam', lazy=True)
    coursesOfStudy = relationship("CourseOfStudy", secondary=CourseOfStudy_has_Course, back_populates="courses")
    professors = relationship("Professor", secondary=Course_has_Professor, back_populates="courses")
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Course(idCourse=%s, name="%s")>' % (self.idCourse, self.name)

    def to_dict(self):
        return {
            'idCourse': self.idCourse,
            'name': self.name,
            'exams': self.exams,
            'coursesOfStudy': self.coursesOfStudy,
            'professors': self.professors
        }

class Exam(Base):
    __tablename__ = 'Exam'

    idExam = Column(Integer, primary_key=True)
    semester = Column(Enum(SemesterEnum), nullable=False)
    year = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    filePath = Column(String(4096), nullable=False)
    isVerified = Column(Boolean, nullable=False, default=False)
    ExamType_idExamType = Column(Integer, ForeignKey('ExamType.idExamType'), nullable=False)
    examType = relationship("ExamType", back_populates='exams', uselist=False)
    Course_idCourse = Column(Integer, ForeignKey('Course.idCourse'), nullable=False)
    course = relationship('Course', back_populates='exams', uselist=False)
    Department_idDepartment = Column(Integer, ForeignKey('Department.idDepartment'), nullable=False)
    department = relationship("Department", back_populates='exams', uselist=False)


    def __init__(self, semester, year, filename, filePath, examType, course, department, isVerified=False):
        self.semester = semester
        self.year = year
        self.filename = filename
        self.filePath = filePath
        self.examType = examType
        self.course = course
        self.department = department
        self.isVerified = isVerified

    def __repr__(self):
        return '<Exam(idExam=%s, semester="%s", year=%d, filename="%s", filePath="%s", examType="%s", isVerified=%d, course="%s", department="%s")>' % (self.idExam, self.semester, self.year, self.filename, self.filePath, self.examType, self.isVerified, self.course, self.department)

    def to_dict(self):
        return {
            'idExam': self.id.Exam,
            'semester': self.semester,
            'year': self.year,
            'filename': self.filename,
            'filePath': self.filePath,
            'isVerified': self.isVerified,
            'course': self.course,
            'department': self.department
        }

class ExamType(Base):
    __tablename__ = 'ExamType'

    idExamType = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    exams = relationship('Exam', back_populates='examType', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ExamType(idExamType=%d, name="%s")>' % (self.idExamType, self.name)

    def to_dict(self):
        return {
            'idExamType': self.idExamType,
            'name': self.name,
            'exams': self.exams
        }