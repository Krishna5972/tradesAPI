from flask import Flask

def create_app():
    app = Flask(__name__)

    from .trading import trading
    app.register_blueprint(trading, url_prefix='/trading')

    with app.app_context():
        from . import routes


    return app

