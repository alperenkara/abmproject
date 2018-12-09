from math import floor, ceil
from typing import List, Tuple, Dict

from vehicle import Vehicle

TIME_STEP = 0.1
TILES_PER_M = 5

DirectionType = str
PosType = Tuple[float, float]


class Lane:
    ExitType = Dict[DirectionType, List[Tuple[PosType, PosType]]]

    def __init__(self, entry: PosType, exits: ExitType):
        self.entry = entry
        self.exits = exits

    def get_curves(self, direction: DirectionType):
        return [lambda t: self._get_func((self.entry,) + exit_points, t) for exit_points in self.exits[direction]]

    def _get_func(self, points: Tuple[PosType, PosType, PosType], t: float):
        p = points
        return (
            (1 - t) * ((1 - t) * p[0][0] + t * p[1][0]) + t * ((1 - t) * p[1][0] + t * p[2][0]),
            (1 - t) * ((1 - t) * p[0][1] + t * p[1][1]) + t * ((1 - t) * p[1][1] + t * p[2][1]),
        )


class Intersection:
    LaneIdType = int
    Time = int
    VehicleType = Vehicle
    TilePos = Tuple[int, int]
    Tile = List[Tuple[Time, VehicleType]]

    def __init__(self, width: int, height: int, lanes: Dict[int, Lane]):
        self.grid = [[[] for _ in range(0, height)] for _ in range(0, width)]
        self.width = width
        self.height = height
        self.current_time = 0
        self.lanes = lanes

    def get_reservation(self, vehicle: VehicleType, lane_id: LaneIdType,
                        requested_direction: DirectionType,
                        speed: float, distance: float) -> bool:
        required_tiles = self._get_lane_tiles(lane_id, requested_direction, speed, vehicle)
        start_at = self.current_time + int(distance / speed / TIME_STEP)
        is_clear = not self._will_collide(required_tiles, start_at)
        if is_clear:
            self._mark_reserved(required_tiles, vehicle, start_at)
        return is_clear

    def _get_vehicle_tiles(self, pos: PosType, vehicle: VehicleType) -> List[TilePos]:  # TODO: buffers
        vehicle_corners = (
            (pos[0] - vehicle.width / 2, pos[1] - vehicle.height / 2),
            (pos[0] + vehicle.width / 2, pos[1] + vehicle.height / 2),
        )

        return [(x, y)
                for x in range(int(floor(vehicle_corners[0][0])), int(ceil(vehicle_corners[1][0])) + 1)
                for y in range(int(floor(vehicle_corners[0][1])), int(ceil(vehicle_corners[1][1])) + 1)]

    # TODO: multiple outgoing lines
    def _get_lane_tiles(self, lane_id: LaneIdType, requested_direction: DirectionType,
                        speed: float, vehicle: VehicleType) -> List[Tuple[TilePos, Time]]:

        lane = self.lanes[lane_id]
        if lane is None:
            return []

        if requested_direction not in lane.exits:
            return []

        t_range = [i * 0.01 for i in range(101)]
        time_to_pass_intersection = 5 / speed  # TODO(15.12): use curve length instead of 5

        return [(tile, int((t * time_to_pass_intersection) / TIME_STEP))
                for curve in lane.get_curves(requested_direction)
                for t in t_range
                for tile in self._get_vehicle_tiles(curve(t), vehicle)]

    def _will_collide(self, required_tiles: List[Tuple[TilePos, Time]],
                      start_at: Time) -> bool:
        return any(time == req_time + start_at
                   for (tile, req_time) in required_tiles
                   for (time, _) in self._get_tile(tile))

    def _get_tile(self, tile: TilePos) -> Tile:
        x, y = tile
        return self.grid[x][y]

    def _mark_reserved(self, required_tiles: List[Tuple[TilePos, Time]],
                       vehicle: VehicleType, start_at: Time):
        for (tile, time) in required_tiles:
            self._get_tile(tile).append((time + start_at, vehicle))
