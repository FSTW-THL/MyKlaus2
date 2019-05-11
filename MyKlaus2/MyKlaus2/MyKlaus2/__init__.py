"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

from MyKlaus2.config import Config
app.config.from_object(Config)

@app.teardown_appcontext
def shutdown_dbsession(exception=None):
    from MyKlaus2.database import db_session
    db_session.remove();

from MyKlaus2.main.routes import main
from MyKlaus2.admin.routes import admin
from MyKlaus2.api.routes import api

app.register_blueprint(main);
app.register_blueprint(admin);
app.register_blueprint(api);
