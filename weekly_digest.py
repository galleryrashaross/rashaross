"""Run weekly (Kubernetes CronJob or Render cron): emails the subscriber list."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

with app.app_context():
    count = app.extensions["digest"].run()
    print(f"Digest sent with {count} subscriber(s).")
