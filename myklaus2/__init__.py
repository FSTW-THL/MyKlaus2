from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '869c27b94136f6faa85afce1dd405997'

    from myklaus2.main.routes import main
    from myklaus2.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app