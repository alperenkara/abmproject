import cmath
import math

from config import PIXES_PER_M


class Vehicle:
    def __init__(self, pos, speed, angle, canvas=None):
        self.pos = pos
        self.speed = speed
        self.angle = angle
        self.width = 2
        self.height = 1
        self.image = None
        self.canvas = canvas
        if canvas is not None:
            self.image = canvas.create_polygon([(0, 0), (1, 0), (0, 1)], fill="blue")

    def tick(self, time):
        distance = self.speed * time
        angle = math.radians(self.angle)
        self.pos = (self.pos[0] + math.cos(angle) * distance,
                    self.pos[1] + math.sin(angle) * distance)

        if self.canvas is not None:
            pos_px = (self.pos[0] * PIXES_PER_M, self.pos[1] * PIXES_PER_M)
            size_px = (self.width * PIXES_PER_M, self.height * PIXES_PER_M)
            center = (pos_px[0] + size_px[0] / 2, pos_px[1] + size_px[1] / 2)
            angle = math.radians(self.angle)
            cangle = cmath.exp(angle * 1j)

            xy = [
                (pos_px[0], pos_px[1] + size_px[1]),
                (pos_px[0], pos_px[1]),
                (pos_px[0] + size_px[0], pos_px[1]),
                (pos_px[0] + size_px[0], pos_px[1] + size_px[1]),
            ]

            offset = complex(center[0], center[1])
            new_xy = []
            for x, y in xy:
                v = cangle * (complex(x, y) - offset) + offset
                new_xy.append(v.real)
                new_xy.append(v.imag)

            self.canvas.coords(self.image, *new_xy)
