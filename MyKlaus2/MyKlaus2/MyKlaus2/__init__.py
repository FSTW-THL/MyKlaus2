"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

from MyKlaus2.config import Config
app.config.from_object(Config)

from MyKlaus2.main.routes import main
from MyKlaus2.admin.routes import admin

app.register_blueprint(main);
app.register_blueprint(admin);
