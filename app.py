import csv
from datetime import datetime

from flask import Flask, render_template, Response, request, jsonify
import cv2
import mediapipe as mp
import numpy as np



app = Flask(__name__)

# Initialize webcam
camera = cv2.VideoCapture(0)

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Global variables
selected_exercise = "bicep_curl"
rep_count = 0
direction = 0
calories_burned = 0
feedback = "Waiting..."
exercise_active = False

# MET values for exercises (in MET units)
MET_VALUES = {
    "bicep_curl": 3.5,   # MET value for light weight training
    "squat": 5.0,        # MET value for squats
    "pushup": 8.0        # MET value for push-ups
}

# User's weight in kilograms (adjust as needed)
WEIGHT_KG = 74

# Exercise configurations
EXERCISE_CONFIGS = {
    "bicep_curl": {
        "landmarks": [11, 13, 15],
        "min_angle": 30,
        "max_angle": 150,
        "feedback_extend": "Extend fully!",
        "feedback_contract": "Good rep!",
        "calorie_multiplier": 0.002
    },
    "squat": {
        "landmarks": [24, 26, 28],
        "min_angle": 70,
        "max_angle": 160,
        "feedback_extend": "Stand up fully!",
        "feedback_contract": "Great depth!",
        "calorie_multiplier": 0.003
    },
    "pushup": {
        "landmarks": [11, 13, 15],
        "min_angle": 50,
        "max_angle": 140,
        "feedback_extend": "Go all the way down!",
        "feedback_contract": "Nice push-up!",
        "calorie_multiplier": 0.0035
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_exercise', methods=['POST'])
def set_exercise():
    global selected_exercise, rep_count, calories_burned, feedback
    data = request.json
    selected_exercise = data['exercise']
    rep_count = 0
    calories_burned = 0
    feedback = "Waiting..."
    return jsonify({"message": f"Exercise set to {selected_exercise}"})

@app.route('/get_stats')
def get_stats():
    return jsonify({"reps": rep_count, "calories": calories_burned, "feedback": feedback})

#-------ADDED RESET FEATURE --------------------
@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    global rep_count, calories_burned, feedback, direction, exercise_active
    rep_count = 0
    calories_burned = 0
    feedback = "Waiting..."
    direction = 0
    exercise_active = False
    return jsonify({"message": "Stats reset successfully."})
session_start_time = None
@app.route('/start_exercise', methods=['POST'])
def start_exercise():
    global exercise_active,session_start_time
    exercise_active = True
    session_start_time = datetime.now()
    return jsonify({"message": "Exercise started."})

@app.route('/stop_exercise', methods=['POST'])
def stop_exercise():
    global exercise_active
    exercise_active = False
    with open(csv_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_start_time, selected_exercise, rep_count, calories_burned])
    return jsonify({"message": "Exercise stopped."})





def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

csv_filename = "latest_workout_log.csv"
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Exercise", "Reps", "Calories"])

def generate_frames():
    global rep_count, direction, calories_burned, feedback

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while True:
            success, frame = camera.read()
            if not success:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark

                if selected_exercise in EXERCISE_CONFIGS and exercise_active:
                    config = EXERCISE_CONFIGS[selected_exercise]
                    shoulder, elbow, wrist = landmarks[config["landmarks"][0]], landmarks[config["landmarks"][1]], landmarks[config["landmarks"][2]]
                    angle = calculate_angle([shoulder.x, shoulder.y], [elbow.x, elbow.y], [wrist.x, wrist.y])

                    if direction == 0 and angle > config["max_angle"]:
                        direction = 1
                        feedback = "Lowering..."

                    elif direction == 1 and angle < config["min_angle"]:
                        rep_count += 1
                        calories_burned += MET_VALUES[selected_exercise] * config["calorie_multiplier"] * WEIGHT_KG
                        feedback = config["feedback_contract"]
                        direction = 0



                    elif direction == 0 and angle < config["min_angle"]:
                        feedback = config["feedback_extend"]


            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)







# from flask import Flask, render_template, Response
# import cv2
# import mediapipe as mp
#
# app = Flask(__name__)
#
# # Initialize Mediapipe Pose
# mp_pose = mp.solutions.pose
# mp_drawing = mp.solutions.drawing_utils
#
# def generate_frames():
#     # Initialize video capture inside function to prevent thread conflicts
#     camera = cv2.VideoCapture(0)
#
#     # Use Mediapipe Pose with specified confidence levels
#     with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
#         while camera.isOpened():
#             success, frame = camera.read()
#             if not success:
#                 break
#
#             # Convert frame from BGR to RGB
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#             # Process the frame with Mediapipe Pose
#             results = pose.process(image)
#
#             # Convert image back to BGR for OpenCV rendering
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#
#             # Draw pose landmarks if detected
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(
#                     image,
#                     results.pose_landmarks,
#                     mp_pose.POSE_CONNECTIONS,
#                     mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                     mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
#                 )
#
#             # Encode processed frame as JPEG
#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#
#             # Yield the frame to the browser
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#     # Release camera after loop exits
#     camera.release()
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template, Response
# import cv2
# import mediapipe as mp
# app = Flask(__name__)
#
# # Initialize webcam feed
# camera = cv2.VideoCapture(0)
#
# # Initialize Mediapipe Pose
# mp_pose = mp.solutions.pose
# mp_drawing = mp.solutions.drawing_utils
#
#
# def generate_frames():
#     # Use Mediapipe Pose with specified confidence levels
#     with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
#         while True:
#             success, frame = camera.read()
#             if not success:
#                 break
#
#             # Convert the frame from BGR to RGB for Mediapipe processing
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False  # Improve performance by marking image as read-only
#
#             # Process the image with Mediapipe Pose
#             results = pose.process(image)
#
#             # Convert the image back to BGR for OpenCV rendering
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#
#             # Draw pose landmarks on the frame if detected
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(
#                     image,
#                     results.pose_landmarks,
#                     mp_pose.POSE_CONNECTIONS,
#                     mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                     mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
#                 )
#
#             # Encode the processed frame as JPEG
#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#
#             # Yield the frame as a byte stream for rendering in the browser
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# if __name__ == '__main__':
#     app.run(debug=True)
