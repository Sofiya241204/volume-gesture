🤚 Hand Gesture Volume Control
Control your system volume using hand gestures captured from a webcam.
This project uses Flask, OpenCV, and MediaPipe to track your hand, and PyAutoGUI to adjust volume.
🚀 Features
Real-time hand tracking with MediaPipe
Volume control using thumb & index finger distance
Webcam streaming directly to browser via Flask
Start/Stop buttons to control video capture
🛠 Technologies Used
Python 3.10+
Flask
OpenCV
MediaPipe
NumPy
PyAutoGUI
HTML / CSS / JavaScript
📂 Project Structure
Copy code

volume-gesture/
├── app.py
├── templates/
│   └── index.html
├── .gitignore
├── LICENSE
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the repository
Copy code
Bash
git clone https://github.com/Sofiya241204/volume-gesture.git
cd volume-gesture
2️⃣ Create a virtual environment (recommended)
Copy code
Bash
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
Copy code
Bash
pip install flask opencv-python mediapipe numpy pyautogui
▶️ Running the Application
Copy code
Bash
python app.py
Open your browser and go to:
Copy code

http://127.0.0.1:5000
✋ How to Use
Click Start to activate the webcam
Show your hand to the camera
Increase volume → move thumb & index finger apart
Decrease volume → move thumb & index finger closer
Click Stop to stop webcam
🔍 How It Works
OpenCV captures webcam frames
MediaPipe detects hand landmarks
Distance between:
Thumb tip (landmark 4)
Index finger tip (landmark 8)
Distance is mapped to volume percentage
PyAutoGUI presses volumeup or volumedown
Flask streams the processed video to the browser
