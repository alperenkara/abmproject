import random
from tkinter import *

from config import PIXES_PER_M
from intersection import Intersection
from vehicle import Vehicle

CANVAS_SIZE = 700
CANVAS_SIZE_M = CANVAS_SIZE // PIXES_PER_M

INTERSECTION_OFFSET = 280
INTERSECTION_OFFSET_M = INTERSECTION_OFFSET // PIXES_PER_M


class Application:
    def __init__(self):
        self.gui = Tk()
        self.gui.title("Autonomous intersection simulation")
        self.gui.geometry("{}x{}".format(CANVAS_SIZE, CANVAS_SIZE))
        self.canvas = Canvas(self.gui, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack()

        self.intersection = Intersection(width=10, height=10)
        self.cars = []
        self.car_spawns = []

        self.init_intersection()

        lane_width = self.intersection.width / 3
        speed_range = range(5, 7, 1)
        for i in range(2):
            self.car_spawns.append((
                [(INTERSECTION_OFFSET_M + lane_width * (2 - i) + lane_width//2,
                  CANVAS_SIZE_M)],
                speed_range, [270], 1 + i, ['E' if i == 0 else 'N']))
        for i in range(2):
            self.car_spawns.append((
                [(INTERSECTION_OFFSET_M + lane_width * i + lane_width // 2,
                  0)],
                speed_range, [90], 4 + i, ['S' if i == 0 else 'E']))

        for i in range(3):
            self.car_spawns.append((
                [(CANVAS_SIZE_M,
                  INTERSECTION_OFFSET_M + lane_width * i + lane_width // 2)],
                speed_range, [180], 7 + i,
                ['N'] if i == 0 else ['N', 'S'] if i == 1 else ['S']))

    def run(self):
        self.gui.after(30, lambda: self._tick(30))
        self.gui.mainloop()

    def _tick(self, time_passed):
        if random.randint(0, 100) < 3:
            spawn = random.choice(self.car_spawns)
            self.cars.append(self.create_car(
                random.choice(spawn[0]),
                random.choice(spawn[1]),
                random.choice(spawn[2])))

        for car in self.cars:
            car.tick(time_passed / 1000)
        self.gui.after(time_passed, lambda: self._tick(time_passed))

    def create_car(self, pos, speed, angle):
        return Vehicle(pos, speed, angle, canvas=self.canvas)

    def init_intersection(self):
        c = self.canvas
        inter = self.intersection

        inter_start_x = INTERSECTION_OFFSET
        inter_start_y = INTERSECTION_OFFSET
        inter_end_x = INTERSECTION_OFFSET + inter.width * PIXES_PER_M
        inter_end_y = INTERSECTION_OFFSET + inter.height * PIXES_PER_M

        # intersection area
        c.create_rectangle(inter_start_x, inter_start_y, inter_end_x, inter_end_y, fill="black")

        # lanes NORTH
        self.create_vertical_lanes(inter_end_x, inter_start_x, 0, inter_start_y)
        # lanes SOUTH
        self.create_vertical_lanes(inter_end_x, inter_start_x, CANVAS_SIZE, inter_end_y)
        # lanes EAST
        self.create_horizontal_lanes(inter_end_y, inter_start_y, CANVAS_SIZE, inter_end_x)

        # external lanes
        c.create_line(inter_end_x, 0, inter_end_x, inter_start_y, fill="red", width=4)
        c.create_line(inter_end_x, inter_end_y, inter_end_x, CANVAS_SIZE, fill="red", width=4)

        c.create_line(inter_end_x, inter_start_y, CANVAS_SIZE, inter_start_y, fill="red", width=4)
        c.create_line(inter_end_x, inter_end_y, CANVAS_SIZE, inter_end_y, fill="red", width=4)

        c.create_line(inter_start_x, 0, inter_start_x, CANVAS_SIZE, fill="red", width=4)

    def create_vertical_lanes(self, inter_end_x, inter_start_x, from_y, to_y):
        c = self.canvas
        lanes_count = 3
        lane_width = (inter_end_x - inter_start_x) // 3
        for i in range(lanes_count):
            lane_start = inter_start_x + i * lane_width
            lane_end = inter_start_x + (i + 1) * lane_width
            c.create_rectangle(lane_start, from_y, lane_end, to_y, fill="#222222")
            if i > 0:
                c.create_line(lane_start, from_y, lane_start, to_y, fill="white")

    def create_horizontal_lanes(self, inter_end_y, inter_start_y, from_x, to_x):
        c = self.canvas
        lanes_count = 3
        lane_width = (inter_end_y - inter_start_y) // 3
        for i in range(lanes_count):
            lane_start = inter_start_y + i * lane_width
            lane_end = inter_start_y + (i + 1) * lane_width
            c.create_rectangle(from_x, lane_start, to_x, lane_end, fill="#222222")
            if i > 0:
                c.create_line(from_x, lane_start, to_x, lane_start, fill="white")
