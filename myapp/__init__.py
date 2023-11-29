from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .trading import trading
    from .mockdata import mockdata

    app.register_blueprint(trading, url_prefix='/trading')
    app.register_blueprint(mockdata, url_prefix='/mockdata')

    with app.app_context():
        from . import routes


    return app

