"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import MyKlaus2.views
from MyKlaus2.admin.routes import admin

app.register_blueprint(admin);
