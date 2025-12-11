import logging.handlers
from flask import Flask, send_from_directory, url_for
import logging
import os

def create_app() -> Flask:
    """
    This function create app and register all blueprints
    And return fully configured app
    """
    
    # Create Flask app instance

    app = Flask(__name__)

    # Logger
    
    app.logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    

    # Headers
    
    @app.after_request
    def add_cors_headers(response):
        # Allow any origin; for stricter control, replace '*' with your allowed origin (e.g., 'https://docu-cup.site')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


    # Register blueprints

    from .code.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix = "")
    from .code.log_in import bp as log_in_bp
    app.register_blueprint(log_in_bp, url_prefix = "/log-in")
    from .code.sign_up import bp as sign_up_bp
    app.register_blueprint(sign_up_bp, url_prefix = "/sign-up")
    from .code.home import bp as home_bp
    app.register_blueprint(home_bp, url_prefix = "/home")
    from .code.add_doc import bp as add_doc_bp
    app.register_blueprint(add_doc_bp, url_prefix = "/add-doc")

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application</h1>'

    return app