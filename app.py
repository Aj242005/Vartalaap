from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
app = Flask(__name__)

# Video capture function
def generate_frames():
    camera = cv2.VideoCapture(0)# 0 means your default webcam
    draw = mp.solutions.drawing_utils
    hands = mp.solutions.hands
    hand_mesh = hands.Hands(static_image_mode=True, min_detection_confidence=0.7)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            op = hand_mesh.process(rgb)
            if op.multi_hand_landmarks:
                for i in op.multi_hand_landmarks:
                    draw.draw_landmarks(frame, i, hands.HAND_CONNECTIONS,landmark_drawing_spec=draw.DrawingSpec(circle_radius=5, color=(0, 250, 250)))



            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Render the UI page

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
