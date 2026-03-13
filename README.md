# EduVision AI – Smart Student Attention & Behavior Analytics System

EduVision AI is an **AI-powered smart classroom monitoring system** designed to analyze student attention, behavior, and engagement in real time using computer vision and machine learning.

The system uses **face recognition, emotion detection, head-pose estimation, and object detection** to evaluate student engagement and classroom productivity.

It provides a **live analytics dashboard** that helps teachers monitor:

* Student attentiveness
* Phone usage violations
* Emotional engagement
* Classroom productivity

EduVision AI aims to bring **AI-driven insights into classrooms**, enabling better teaching strategies and improved student engagement.

---

# Key Features

### Real-Time Student Detection

Detects students in the classroom using **YOLOv8 object detection** and tracks them using **DeepSORT tracking**.

### Face Recognition

Identifies registered students using **FaceNet embeddings via DeepFace**.

### Attention Analysis

Evaluates student attentiveness based on:

* Head pose direction
* Facial emotion
* Phone usage detection

### Emotion Detection

Detects emotions such as:

* Happy
* Neutral
* Sad
* Angry
* Surprise

### Phone Usage Detection

Detects mobile phone usage using object detection and logs violations.

### Behavior Alerts

Automatically generates alerts for:

* Using phone
* Sleeping in class
* Raising hand

### Classroom Productivity Score

Calculates overall classroom productivity based on student attention scores.

### Attendance System

Automatically marks attendance when a registered student is detected.

### Evidence Capture

When phone usage is detected, the system captures image evidence and logs it.

### Live Dashboard

Displays:

* Live classroom feed
* Attention trend graph
* Emotion distribution
* Behavior alerts
* Phone violation logs

---

# System Architecture

EduVision AI consists of three main modules:

### 1. AI Engine

Handles:

* Video processing
* Object detection
* Face recognition
* Attention scoring
* Behavior analysis

### 2. Backend API

Built using **FastAPI**.

Provides APIs for:

* Classroom statistics
* Emotion analytics
* Alerts
* Phone violation logs

### 3. Dashboard

Web interface showing real-time analytics using:

* HTML
* CSS
* JavaScript
* Chart.js

---

# Project Structure

```
EduVision-AI
│
├── ai_engine
│   └── eduvision_engine.py
│
├── student_recognition
│   ├── dataset
│   ├── embeddings
│   ├── register_student.py
│   ├── train_faces.py
│   └── recognize_faces.py
│
├── dashboard
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── phone_evidence
│
├── stats.json
├── alerts.json
├── emotion_stats.json
├── phone_violations.csv
├── attendance.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technologies Used

### Computer Vision

* YOLOv8 (Ultralytics)
* OpenCV
* DeepFace (FaceNet embeddings)
* MediaPipe (Pose estimation)

### Machine Learning

* Face recognition using embeddings
* Emotion detection
* Attention scoring algorithms

### Tracking

* DeepSORT real-time multi-object tracking

### Backend

* FastAPI
* Flask (video streaming)

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

---

# How the System Works

### Step 1 – Student Registration

Students are registered by capturing multiple face images.

```
python student_recognition/register_student.py
```

This creates a dataset folder for each student.

---

### Step 2 – Face Embedding Training

Generate face embeddings from the captured images.

```
python student_recognition/train_faces.py
```

This creates:

```
embeddings/face_embeddings.pkl
```

---

### Step 3 – Start Backend API

```
uvicorn backend:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### Step 4 – Start AI Engine

```
python ai_engine/eduvision_engine.py
```

This starts:

* AI processing
* Video streaming
* Attention analytics

Video stream available at:

```
http://127.0.0.1:5000/video
```

---

### Step 5 – Open Dashboard

Open:

```
dashboard/index.html
```

The dashboard shows:

* Live classroom feed
* Attention trend graph
* Emotion distribution
* Behavior alerts
* Phone violation logs

---

# Requirements

Install all dependencies using:

```
pip install -r requirements.txt
```

Main dependencies include:

* ultralytics
* opencv-python
* numpy
* deepface
* mediapipe
* fastapi
* flask
* uvicorn
* deep-sort-realtime
* tensorflow

---

# Example Dashboard Insights

The dashboard provides real-time analytics such as:

### Student Count

Total number of detected students.

### Average Attention Score

Calculated from student behavior metrics.

### Phone Violations

Students using phones are logged with image evidence.

### Emotion Distribution

Pie chart showing emotional state of students.

### Behavior Alerts

Real-time alerts for:

* sleeping
* phone usage
* raised hands

---

# Future Improvements

Possible improvements include:

* Multi-camera classroom support
* Advanced attention modeling
* Teacher analytics dashboard
* Mobile app integration
* Cloud deployment
* AI-based lecture effectiveness analysis

---

# Use Cases

* Smart classrooms
* Online exam monitoring
* Student engagement analytics
* AI-assisted teaching systems
* Educational research

---

# Authors

Developed by:

Sai Vadlakonda,

BharathSai Yada,

Anjana Reddy Sathu

---

# License

This project is developed for educational and research purposes.
