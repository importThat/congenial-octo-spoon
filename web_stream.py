import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

from flask import Flask, Response
import pygame
import numpy as np
import cv2
import time
import importlib.util

WIDTH, HEIGHT = 640, 480
AGENT_FOLDER = "./agents"

app = Flask(__name__)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

agents = []

@app.route("/video")
def video_feed():
    def generate():
        while True:
            screen.fill((0,0,0))

            pygame.draw.circle(screen,(255,0,0),(320,240),40)

            frame = pygame.surfarray.array3d(screen)
            frame = np.transpose(frame,(1,0,2))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            _, jpeg = cv2.imencode('.jpg', frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   jpeg.tobytes() +
                   b'\r\n')

            time.sleep(0.03)

    return Response(generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)