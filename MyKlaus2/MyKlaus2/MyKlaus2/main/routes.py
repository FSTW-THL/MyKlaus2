from datetime import datetime
from flask import Blueprint, render_template
from sqlalchemy import func
from sqlalchemy_paginator import Paginator
from MyKlaus2.database import db_session
from MyKlaus2.models import Exam, Department, Course

main = Blueprint("main", __name__);

@main.route('/')
def home():
    departments = []
    deps = db_session.query(Department.idDepartment, Department.name, func.count(Exam.Department_idDepartment)).join(Department, Exam.department).group_by(Exam.Department_idDepartment).order_by(Department.name).all()
    for dep in deps:
        cours = db_session.query(Course.name, func.count(Exam.Course_idCourse)).join(Course, Exam.course).filter(Course.Department_idDepartment == dep.idDepartment).group_by(Exam.Course_idCourse).order_by(Course.name).all()
        courses = []
        for cour in cours:
            courses.append({
                'name': cour.name,
                'count': cour[1]
            })
        departments.append({
            'name': dep.name,
            'count': dep[2],
            'courses': courses
        })

    return render_template(
        'index.html',
        title='Home Page',
        showing='Dokumente',
        departments=departments
    )

@main.route('/list')
def list():
    return render_template(
        'list.html',
        title='Merkliste',
        showing='Merkliste'
    )

@main.route('/feedback')
def feedback():
    return "FEEDBACK"

@main.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        showing='Your contact page.'
    )

@main.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        showing='Your application description page.'
    )
