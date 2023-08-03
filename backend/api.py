from flask import Flask, Response, jsonify
from flask_cors import CORS, cross_origin
import cv2
import os
import time

application = Flask(__name__)
application.config['CORS_HEADERS'] = 'Content-Type'
application.config["CORS_ORIGINS"] = ["http://localhost:4200","http://127.0.0.1:4200"] 
cors = CORS(application)

def generate_frames(file_path):
    camera = cv2.VideoCapture(file_path)

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Process the frame here if needed

        print(frame.shape)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(1 / 24)  # Change 30 to your desired frame rate

    camera.release()

@application.route('/start_streaming', methods=['POST'])
@cross_origin()
def start_streaming():
    # Start the streaming when this endpoint is called
    video_url = '/video_feed'
    return jsonify({'video_url': video_url})

@application.route('/video_feed')
@cross_origin()
def video_feed():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_name = 'video.mp4'  # Replace with the name of your video file
    file_path = os.path.join(current_folder, file_name)
    print(file_path)
    return Response(generate_frames(file_path), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    application.run(debug=True)