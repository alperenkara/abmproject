from typing import List, Tuple

TIME_STEP = 1
TILE_SIZE = 5  # m


class Intersection:
    LaneIdType = int
    Time = int
    VehicleType = int
    TilePos = Tuple[int, int]
    Tile = List[Tuple[Time, VehicleType]]

    def __init__(self, width: int, height: int):
        self.grid = [[[] for _ in range(0, height)] for _ in range(0, width)]
        self.width = width
        self.height = height
        self.current_time = 0

    def get_reservation(self, vehicle: VehicleType, lane_id: LaneIdType,
                        requested_direction,
                        speed: float, distance: float) -> bool:
        required_tiles = self._get_lane_tiles(lane_id, speed / TILE_SIZE)
        start_at = self.current_time + int(distance / speed)
        is_clear = not self._will_collide(required_tiles, start_at)
        if is_clear:
            self._mark_reserved(required_tiles, vehicle, start_at)
        return is_clear

    def _get_lane_tiles(self, lane_id: LaneIdType,
                        tile_speed: float) -> List[Tuple[TilePos, Time]]:
        result = []
        if lane_id == 1:
            result = [((x, y), time)
                      for x in range(self.width // 2, self.width)
                      for y in range(0, self.height)
                      for time in range(int(y / tile_speed),
                                        int((y + 1) / tile_speed))]
        elif lane_id == 3:
            result = [((x, y), time)
                      for x in range(0, int(self.width / 2))
                      for y in range(0, self.height)
                      for time in range(int((self.height - y - 1) / tile_speed),
                                        int((self.height - y) / tile_speed))]
        elif lane_id == 2:
            result = [((x, y), time)
                      for x in range(0, self.width)
                      for y in range(0, int(self.height / 2))
                      for time in range(int(x / tile_speed),
                                        int((x + 1) / tile_speed))]
        elif lane_id == 4:
            result = [((x, y), time)
                      for x in range(0, self.width)
                      for y in range(0, int(self.height / 2))
                      for time in range(int((self.width - x - 1) / tile_speed),
                                        int((self.width - x) / tile_speed))]

        return result

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
