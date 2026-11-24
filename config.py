"""Central configuration. All secrets come from environment variables
(set in render.yaml on Render, or the k8s Secret in the cluster)."""
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME", "")

    # Where the weekly subscriber list is delivered
    DIGEST_RECIPIENT = os.environ.get("DIGEST_RECIPIENT", "")

    DATABASE_PATH = os.environ.get("DATABASE_PATH", "data/subscribers.db")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")  # set by Render Postgres
    CONTENT_DIR = os.environ.get("CONTENT_DIR", "content")
    ARTIST_NAME = "Rasha Ross"
