import random
from tkinter import *

from config import PIXES_PER_M, INTERSECTION_OFFSET_M, INTERSECTION_OFFSET
from intersection import Intersection, Lane
from vehicle import Vehicle

# TODO: Vehicles do not collides with each other
# TODO(15.12): Vehicles ask for clearance at intersection
# TODO(15.12): Vehicles slows down if don't have clearance
# TODO(15.12)?: Vehicles change angle lanes at intersection
# TODO(15.12)?: Use better curves for lanes, exact entry and exit points

CANVAS_SIZE = 700
CANVAS_SIZE_M = CANVAS_SIZE // PIXES_PER_M


def mid_pos(lane_width: float, i: int):
    return lane_width * (i - 1) + lane_width / 2


class CzarnowiejskaIntersection(Intersection):

    def __init__(self):
        width = 10
        height = 10
        lane_width = height / 3
        lanes = {
            1: Lane((mid_pos(lane_width, 3), height), {
                'E': [((mid_pos(lane_width, 3), mid_pos(lane_width, 3)),
                      (width, mid_pos(lane_width, 3)))]
            }),
            2: Lane((mid_pos(lane_width, 2), height), {
                'N': [((mid_pos(lane_width, 2), height / 2),
                      (mid_pos(lane_width, 3), 0))]
            }),
            4: Lane((mid_pos(lane_width, 1), 0), {
                'S': [((mid_pos(lane_width, 1), height / 2),
                      (mid_pos(lane_width, 1), height))]
            }),
            5: Lane((mid_pos(lane_width, 2), 0), {
                'E': [((mid_pos(lane_width, 2), mid_pos(lane_width, 2)),
                      (width, mid_pos(lane_width, 2)))]
            }),
            7: Lane((width, mid_pos(lane_width, 1)), {
                'N': [((mid_pos(lane_width, 3), mid_pos(lane_width, 1)),
                      (mid_pos(lane_width, 3), 0))]
            }),
            8: Lane((width, mid_pos(lane_width, 2)), {
                'S': [((mid_pos(lane_width, 1), mid_pos(lane_width, 2)),
                      (mid_pos(lane_width, 1), height))]
            }),
        }
        super(CzarnowiejskaIntersection, self).__init__(width=width, height=height, lanes=lanes)


class Application:
    def __init__(self):
        self.gui = Tk()
        self.gui.title("Autonomous intersection simulation")
        self.gui.geometry("{}x{}".format(CANVAS_SIZE, CANVAS_SIZE))
        self.canvas = Canvas(self.gui, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack()

        self.intersection = CzarnowiejskaIntersection()
        self.cars = []
        self.car_spawns = []

        self.init_intersection()

        # TODO: rework spawn points
        lane_width = self.intersection.width / 3
        # speed_range = range(5, 7, 1)
        speed_range = [6]
        for i in range(2):
            self.car_spawns.append((
                (INTERSECTION_OFFSET_M + lane_width * (2 - i) + lane_width // 2, CANVAS_SIZE_M),
                speed_range, 270, 1 + i, 'E' if i == 0 else 'N',
                (INTERSECTION_OFFSET_M + lane_width * (2 - i) + lane_width // 2,
                 INTERSECTION_OFFSET_M + self.intersection.height)
            ))
        for i in range(2):
            self.car_spawns.append((
                (INTERSECTION_OFFSET_M + lane_width * i + lane_width // 2, 0),
                speed_range, 90, 4 + i, 'S' if i == 0 else 'E',
                (INTERSECTION_OFFSET_M + lane_width * i + lane_width // 2, INTERSECTION_OFFSET_M)
            ))

        for i in range(2):
            self.car_spawns.append((
                (CANVAS_SIZE_M, INTERSECTION_OFFSET_M + lane_width * i + lane_width // 2),
                speed_range, 180, 7 + i, 'N' if i == 0 else 'S',
                (INTERSECTION_OFFSET_M + self.intersection.width,
                 INTERSECTION_OFFSET_M + lane_width * i + lane_width // 2)
            ))

    def run(self):
        spawn = random.choice(self.car_spawns)
        self.cars.append(Vehicle(
            spawn[0],
            random.choice(spawn[1]),
            spawn[2],
            spawn[3],
            spawn[4],
            spawn[5],
            self.intersection,
            self.canvas
        ))
        self.gui.after(30, lambda: self._tick(30))
        self.gui.mainloop()

    def _tick(self, time_passed):
        if random.randint(0, 100) < 3:
            spawn = random.choice(self.car_spawns)
            self.cars.append(Vehicle(
                spawn[0],
                random.choice(spawn[1]),
                spawn[2],
                spawn[3],
                spawn[4],
                spawn[5],
                self.intersection,
                self.canvas
            ))

        for car in self.cars:
            car.tick(time_passed / 1000)
        self.gui.after(time_passed, lambda: self._tick(time_passed))

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
