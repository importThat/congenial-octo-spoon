# web_stream.py
# Serves a minimal web steam in http://<VM-IP>:<NodePort>/video
from flask import Flask, Response
import cv2
import pygame
import numpy as np

app = Flask(__name__)
pygame.init()
screen = pygame.Surface((640, 480))  # offscreen

@app.route("/video")
def video_feed():
    def generate():
        while True:
            # Draw something minimal
            screen.fill((0,0,0))
            pygame.draw.circle(screen, (255,0,0), (320,240), 50)
            # Convert to image
            data = pygame.surfarray.array3d(screen)
            frame = cv2.cvtColor(np.transpose(data, (1,0,2)), cv2.COLOR_RGB2BGR)
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host="0.0.0.0", port=8080)