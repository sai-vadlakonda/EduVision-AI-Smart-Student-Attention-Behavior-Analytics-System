from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
import csv

app = FastAPI()

# -----------------------------
# Enable CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# File locations
# -----------------------------

STATS_FILE = "stats.json"
ALERTS_FILE = "alerts.json"
EMOTIONS_FILE = "emotion_stats.json"

PHONE_EVIDENCE_DIR = "phone_evidence"
PHONE_LOG_FILE = "phone_violations.csv"
ALERT_LOG_FILE = "alerts_log.csv"

# -----------------------------
# Ensure evidence folder exists
# -----------------------------

os.makedirs(PHONE_EVIDENCE_DIR, exist_ok=True)

# -----------------------------
# Serve evidence images
# -----------------------------

app.mount("/evidence", StaticFiles(directory=PHONE_EVIDENCE_DIR), name="evidence")


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def home():
    return {"status": "EduVision AI Backend Running"}


# -----------------------------
# Classroom Stats
# -----------------------------

@app.get("/stats")
def get_stats():

    if not os.path.exists(STATS_FILE):
        return {
            "students": 0,
            "attention": 0,
            "phones": 0,
            "productivity": 0
        }

    with open(STATS_FILE, "r") as f:
        return json.load(f)


# -----------------------------
# Alerts
# -----------------------------

@app.get("/alerts")
def get_alerts():

    if not os.path.exists(ALERTS_FILE):
        return []

    with open(ALERTS_FILE, "r") as f:
        return json.load(f)


# -----------------------------
# Emotion Analytics
# -----------------------------

@app.get("/emotions")
def get_emotions():

    if not os.path.exists(EMOTIONS_FILE):
        return {}

    with open(EMOTIONS_FILE, "r") as f:
        return json.load(f)


# -----------------------------
# Phone Violations Logs
# -----------------------------

@app.get("/phone_logs")
def get_phone_logs():

    if not os.path.exists(PHONE_LOG_FILE):
        return []

    logs = []

    with open(PHONE_LOG_FILE, "r") as f:

        reader = csv.DictReader(f)

        for row in reader:

            image_file = row.get("Image", "")

            logs.append({
                "Time": row.get("Time", ""),
                "RollNo": row.get("RollNo", ""),
                "Student": row.get("Student", ""),
                "Image": image_file,
                "ImageURL": f"http://127.0.0.1:8000/evidence/{image_file}"
            })

    return logs


# -----------------------------
# Alert Logs
# -----------------------------

@app.get("/alert_logs")
def get_alert_logs():

    if not os.path.exists(ALERT_LOG_FILE):
        return []

    logs = []

    with open(ALERT_LOG_FILE, "r") as f:

        reader = csv.DictReader(f)

        for row in reader:
            logs.append(row)

    return logs