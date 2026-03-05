import cv2

class BlueCircle:

    def __init__(self, width, height):
        self.x = 100
        self.y = height // 2
        self.radius = 30
        self.speed = 5
        self.direction = 1
        self.width = width

    def update(self):

        self.x += self.speed * self.direction

        if self.x + self.radius > self.width or self.x - self.radius < 0:
            self.direction *= -1

    def draw(self, frame):

        cv2.circle(
            frame,
            (self.x, self.y),
            self.radius,
            (255,0,0),
            -1
        )