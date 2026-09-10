from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.config import setup_logging
    setup_logging()

    from app.routes.generate import generate_bp
    app.register_blueprint(generate_bp, url_prefix="/api")

    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

    @app.route("/api/health")
    def health():
        return {"status": "healthy"}, 200

    return app