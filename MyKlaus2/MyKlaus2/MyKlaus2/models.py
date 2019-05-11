from sqlalchemy import Table, Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from MyKlaus2.database import Base
import enum
import json

#Enums
class SemesterEnum(enum.Enum):
    SS = 'SS'
    WS = 'WS'

#Tabellen
class Department(Base):
    __tablename__ = 'Department'

    idDepartment = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    exams = relationship('Exam', back_populates='department', lazy=True, order_by='desc(Exam.year)')
    courses = relationship('Course', back_populates='department', lazy=False, order_by='Course.name')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Department(idDepartment=%d, name="%s">' % (self.idDepartment, self.name)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def to_serializable_dict(self):
        return {
            'idDepartment': self.idDepartment,
            'name': self.name
        }

    def to_dict(self):
        return {
            'idDepartment': self.idDepartment,
            'name': self.name,
            'exams': self.exams,
            'courses': self.courses
        }

class Professor(Base):
    __tablename__ = 'Professor'

    idProfessor = Column(Integer, primary_key=True)
    firstName = Column(String(128))
    lastName = Column(String(128), nullable=False)
    isAgainstMyKlaus = Column(Boolean, nullable=False, default=False)
    exams = relationship('Exam', back_populates='professor', lazy=True, order_by='desc(Exam.year)')

    def __init__(self, lastName, firstName=None, isAgainstMyKlaus=True):
        self.firstName = firstName
        self.lastName = lastName
        self.isAgainstMyKlaus = isAgainstMyKlaus

    def __repr__(self):
        return '<Professor(idProfessor=%d, firstName="%s", lastName="%s", isAgainstMyKlaus=%d)>' % (self.idProfessor, self.firstName, self.lastName, self.isAgainstMyKlaus)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def to_serializable_dict(self):
        return {
            'idProfessor': self.idProfessor,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'isAgainstMyKlaus': self.isAgainstMyKlaus
        }

    def to_dict(self):
        return {
            'idProfessor': self.idProfessor,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'isAgainstMyKlaus': self.isAgainstMyKlaus,
            'exams': self.exams
        }

class Course(Base):
    __tablename__ = 'Course'

    idCourse = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    exams = relationship('Exam', back_populates='course', lazy=True, order_by='desc(Exam.year)')
    Department_idDepartment = Column(Integer, ForeignKey('Department.idDepartment'), nullable=False)
    department = relationship("Department", back_populates='courses', uselist=False)

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def __repr__(self):
        return '<Course(idCourse=%s, name="%s")>' % (self.idCourse, self.name)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def to_serializable_dict(self):
        return {
            'idCourse': self.idCourse,
            'name': self.name
        }

    def to_dict(self):
        return {
            'idCourse': self.idCourse,
            'name': self.name,
            'exams': self.exams
        }

class ExamType(Base):
    __tablename__ = 'ExamType'

    idExamType = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    exams = relationship('Exam', back_populates='examType', lazy=True, order_by='desc(Exam.year)')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ExamType(idExamType=%d, name="%s")>' % (self.idExamType, self.name)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def to_serializable_dict(self):
        return {
            'idExamType': self.idExamType,
            'name': self.name
        }

    def to_dict(self):
        return {
            'idExamType': self.idExamType,
            'name': self.name,
            'exams': self.exams
        }

class Exam(Base):
    __tablename__ = 'Exam'

    idExam = Column(Integer, primary_key=True)
    semester = Column(Enum(SemesterEnum), nullable=False)
    year = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    filePath = Column(String(4096), nullable=False)
    isVerified = Column(Boolean, nullable=False, default=False)
    Course_idCourse = Column(Integer, ForeignKey('Course.idCourse'), nullable=False)
    course = relationship("Course", back_populates='exams', uselist=False)
    Department_idDepartment = Column(Integer, ForeignKey('Department.idDepartment'), nullable=False)
    department = relationship("Department", back_populates='exams', uselist=False)
    ExamType_idExamType = Column(Integer, ForeignKey('ExamType.idExamType'), nullable=False)
    examType = relationship("ExamType", back_populates='exams', uselist=False)
    Professor_idProfessor = Column(Integer, ForeignKey('Professor.idProfessor'), nullable=False)
    professor = relationship("Professor", back_populates='exams', uselist=False)


    def __init__(self, semester, year, filename, filePath, course, department, examType, professor, isVerified=False):
        self.semester = semester
        self.year = year
        self.filename = filename
        self.filePath = filePath
        self.examType = examType
        self.course = course
        self.department = department
        self.professor = professor
        self.isVerified = isVerified

    def __repr__(self):
        return '<Exam(idExam=%s, semester="%s", year=%d, filename="%s", filePath="%s", examType="%s", isVerified=%d, course="%s", department="%s")>' % (self.idExam, self.semester, self.year, self.filename, self.filePath, self.examType, self.isVerified, self.course, self.department)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def to_serializable_dict(self):
        return {
            'idExam': self.idExam,
            'semester': self.semester.name,
            'year': self.year,
            'filename': self.filename,
            'filePath': self.filePath,
            'isVerified': self.isVerified,
            'course': self.course.to_serializable_dict(),
            'department': self.department.to_serializable_dict(),
            'examType': self.examType.to_serializable_dict(),
            'professor': self.professor.to_serializable_dict()
        }

    def to_dict(self):
        return {
            'idExam': self.idExam,
            'semester': self.semester.name,
            'year': self.year,
            'filename': self.filename,
            'filePath': self.filePath,
            'isVerified': self.isVerified,
            'examType': self.examType,
            'course': self.course,
            'department': self.department,
            'examType': self.examType,
            'professor': self.professor
        }