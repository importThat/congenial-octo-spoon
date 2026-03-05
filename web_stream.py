from flask import Flask, Response
import pygame
import numpy as np
import cv2
import time
import importlib.util
import os

# Settings
WIDTH, HEIGHT = 640, 480
AGENT_FOLDER = "./agents"

os.environ["SDL_VIDEODRIVER"] = "dummy"
# Initialize Flask and Pygame
app = Flask(__name__)
pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))

# Load all agents dynamically
agents = []
for file in os.listdir(AGENT_FOLDER):
    if file.endswith(".py"):
        filepath = os.path.join(AGENT_FOLDER, file)
        spec = importlib.util.spec_from_file_location(file[:-3], filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Instantiate the first class found in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type):  # check if it is a class
                agent_instance = attr(WIDTH, HEIGHT)
                agents.append(agent_instance)
                break  # only first class per file

@app.route("/video")
def video_feed():
    def generate():
        while True:
            screen.fill((0, 0, 0))  # clear screen

            # Update and draw all agents
            for agent in agents:
                agent.update()
                agent.draw(screen)

            # Convert pygame surface to OpenCV image
            frame = pygame.surfarray.array3d(screen)
            frame = np.transpose(frame, (1, 0, 2))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Encode as JPEG
            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()

            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.03)

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)