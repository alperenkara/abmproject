from tkinter import *

from intersection import Intersection

CANVAS_SIZE = 1000

PIXES_PER_M = 32
INTERSECTION_OFFSET = 260


class Application:
    def __init__(self):
        self.gui = Tk()
        self.gui.title("Autonomous intersection simulation")
        self.gui.geometry("{}x{}".format(CANVAS_SIZE, CANVAS_SIZE))
        self.canvas = Canvas(self.gui, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack()

        self.intersection = Intersection(width=10, height=10)

        self.init_intersection()

    def run(self):
        self.gui.mainloop()

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
        self.create_vertical_lanes(inter_end_x, inter_start_x, inter_end_y, CANVAS_SIZE)
        # lanes EAST
        self.create_horizontal_lanes(inter_end_y, inter_start_y, inter_end_x, CANVAS_SIZE)

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

