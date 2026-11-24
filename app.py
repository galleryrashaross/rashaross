"""Main entry point: wires configuration, content, services and routes."""
from flask import Flask, render_template, request, jsonify

from config import Config
from core.content_loader import ContentLoader
from core.repository import SubscriberRepository
from core.mailer import Mailer
from core.digest import WeeklyDigest


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    loader = ContentLoader(app.config["CONTENT_DIR"])
    repo = SubscriberRepository(app.config["DATABASE_PATH"])
    mailer = Mailer(app)
    app.extensions["digest"] = WeeklyDigest(
        repo, mailer, app.config["DIGEST_RECIPIENT"])

    @app.get("/")
    def index():
        return render_template("index.html", sections=loader.load_sections(),
                               artist=app.config["ARTIST_NAME"])

    @app.post("/subscribe")
    def subscribe():
        email = (request.form.get("email") or "").strip().lower()
        if not repo.is_valid(email):
            return jsonify(ok=False, message="Please enter a valid email."), 400
        if repo.add(email):
            try:
                mailer.send_welcome(email)
            except Exception:
                app.logger.exception("Welcome email failed")
        return jsonify(ok=True, message="Thank you for subscribing.")

    @app.get("/healthz")
    def health():
        return "ok"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
