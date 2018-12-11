import cmath
import math
from typing import Tuple

from config import PIXES_PER_M, INTERSECTION_OFFSET_M

PosType = Tuple[float, float]


def dist(a: PosType, b: PosType) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class Vehicle:
    def __init__(self, pos, speed, angle, lane_id, intended_direction, inter_entry, inter, canvas=None):
        self.pos = pos
        self.speed = speed
        self.angle = angle
        self.lane_id = lane_id
        self.intended_direction = intended_direction
        self.inter_entry = inter_entry
        self.inter = inter
        self.width = 2
        self.height = 1
        self.at_inter_since = None
        self.intersection_path = None
        self.image = None
        self.canvas = canvas
        if canvas is not None:
            self.image = canvas.create_polygon([(0, 0), (1, 0), (0, 1)], fill="blue")

    def tick(self, time):
        if self.intersection_path is None:
            self.intersection_path = self.inter.get_reservation(
                self, self.lane_id, self.intended_direction,
                self.speed, dist(self.pos, self.inter_entry))

        if self.at_inter_since is not None:
            self.at_inter_since += time
            x, y = self.intersection_path[0](self.at_inter_since/self.intersection_path[1])
            self.pos = (INTERSECTION_OFFSET_M + x, INTERSECTION_OFFSET_M + y)
            if self.at_inter_since >= self.intersection_path[1]:
                self.at_inter_since = None
                if self.intended_direction == 'S':
                    self.angle = 90
                elif self.intended_direction == 'E':
                    self.angle = 0
                elif self.intended_direction == 'N':
                    self.angle = 270

        else:
            distance = self.speed * time
            angle = math.radians(self.angle)
            self.pos = (self.pos[0] + math.cos(angle) * distance,
                        self.pos[1] + math.sin(angle) * distance)

            if dist(self.pos, self.inter_entry) < 0.1:
                self.at_inter_since = 0

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
