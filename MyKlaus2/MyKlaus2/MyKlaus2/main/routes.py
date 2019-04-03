from datetime import datetime
from flask import Blueprint, render_template


main = Blueprint("main", __name__);

@main.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        showing='Fächer',
        year=datetime.now().year,
    )

@main.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        showing='Your contact page.'
    )

@main.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        showing='Your application description page.'
    )
