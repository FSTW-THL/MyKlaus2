from datetime import datetime
from flask import Blueprint, render_template
from MyKlaus2.database import db_session
from MyKlaus2.models import Exam, Department


main = Blueprint("main", __name__);

@main.route('/')
@main.route('/<string:search>', methods=['GET', 'POST'])
def home(search=None):
    departments = db_session.query(Department).order_by(Department.name).all()
    return render_template(
        'index.html',
        title='Home Page',
        showing='Fächer',
        departments=departments,
    )

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
