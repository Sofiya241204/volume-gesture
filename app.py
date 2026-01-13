from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import math
import pyautogui
import numpy as np

app = Flask(__name__)

# MediaPipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Global variables
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
running = True  # controls whether webcam frames are being processed

def calculate_distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

def generate_frames():
    global cap, running
    while True:
        if not running:
            continue  # Skip frames when stopped

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lm_list.append((cx, cy))

                if lm_list:
                    thumb_tip = lm_list[4]
                    index_tip = lm_list[8]

                    # Draw landmarks
                    cv2.circle(frame, thumb_tip, 10, (255,0,0), cv2.FILLED)
                    cv2.circle(frame, index_tip, 10, (255,0,0), cv2.FILLED)
                    cv2.line(frame, thumb_tip, index_tip, (0,255,0), 3)

                    # Distance and volume mapping
                    distance = calculate_distance(thumb_tip, index_tip)
                    volume = int(np.interp(distance, [20,200],[0,100]))

                    # Press keys based on distance
                    if volume > 50:
                        pyautogui.press('volumeup')
                    else:
                        pyautogui.press('volumedown')

                    cv2.putText(frame, f'Volume: {volume}%', (50,50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start():
    global running
    running = True
    return ('', 204)

@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    return ('', 204)

# Release webcam on shutdown
@app.route('/shutdown', methods=['POST'])
def shutdown():
    global cap
    if cap:
        cap.release()
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)
