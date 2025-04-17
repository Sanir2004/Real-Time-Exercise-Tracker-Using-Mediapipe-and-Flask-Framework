# Real-Time-Exercise-Tracker-Using-Mediapipe-and-Flask-Framework

# 💪 Smart Exercise Tracker using Flask + Mediapipe

This project is a real-time exercise monitoring web app built using **Flask**, **OpenCV**, and **MediaPipe**. It uses your webcam to track body movements and gives live feedback for exercises like **bicep curls**, **squats**, and **push-ups**. It also counts reps and estimates calories burned!

---

## 🚀 Features

- 🎥 Real-time pose detection via webcam  
- 💡 Intelligent feedback based on joint angles  
- 🔢 Repetition counting  
- 🔥 Calories estimation based on MET values  
- 📊 Live stats panel (reps, calories, feedback)  
- 🔁 Start, stop, and reset workout sessions  
- 📝 Auto-logging workout data into CSV  

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **Computer Vision**: OpenCV, MediaPipe  
- **Frontend**: HTML, JavaScript (Flask templating)  
- **Data Logging**: CSV  

---

## ⚙️ Installation & Running Locally

> Make sure you have Python 3.7+ installed.

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/exercise-tracker-flask.git
   cd exercise-tracker-flask

   pip install -r requirements.txt

   python app.py
