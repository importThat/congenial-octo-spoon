from flask import Flask, Response
import pygame
import numpy as np
import cv2
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize Pygame surface (offscreen)
WIDTH, HEIGHT = 640, 480
pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))

# Circle state
circle_x = 50
circle_y = HEIGHT // 2
circle_radius = 50
speed = 5
direction = 1  # 1 = right, -1 = left

@app.route("/video")
def video_feed():
    def generate():
        global circle_x, direction

        while True:
            # Move circle
            circle_x += speed * direction
            if circle_x + circle_radius >= WIDTH or circle_x - circle_radius <= 0:
                direction *= -1  # bounce back

            # Draw background and circle
            screen.fill((0, 0, 0))
            pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), circle_radius)

            # Convert pygame surface to OpenCV image
            frame = pygame.surfarray.array3d(screen)
            frame = np.transpose(frame, (1, 0, 2))  # Pygame surface is (width, height)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Encode as JPEG
            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()

            # Yield frame for MJPEG stream
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            time.sleep(0.03)  # ~30 FPS

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Run Flask app on all interfaces
    app.run(host="0.0.0.0", port=8080)