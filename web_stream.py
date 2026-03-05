from flask import Flask, Response
import numpy as np
import cv2
import time
import importlib.util
import os

WIDTH, HEIGHT = 640, 480
AGENT_FOLDER = "./agents"

app = Flask(__name__)

agents = []

# Dynamically load agents
for file in os.listdir(AGENT_FOLDER):
    if file.endswith(".py"):
        path = os.path.join(AGENT_FOLDER, file)
        spec = importlib.util.spec_from_file_location(file[:-3], path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type):
                agents.append(attr(WIDTH, HEIGHT))
                break


@app.route("/video")
def video():

    def generate():
        while True:

            # Create blank frame
            frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

            # Update and draw agents
            for agent in agents:
                agent.update()
                agent.draw(frame)

            _, jpeg = cv2.imencode(".jpg", frame)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + jpeg.tobytes()
                + b"\r\n"
            )

            time.sleep(0.03)

    return Response(generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)