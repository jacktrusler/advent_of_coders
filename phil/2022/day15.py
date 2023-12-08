from time import perf_counter_ns
from math import floor, ceil
from itertools import combinations


class Sensor:
    def __init__(self, x, y, search_range):
        self.x = x
        self.y = y
        self.search_range = search_range
        self.x_min = x - search_range
        self.x_max = x + search_range
        self.y_min = y - search_range
        self.y_max = y + search_range
        self.lower_left = Segment(slope=-1, y_intercept=y+self.x_min-1,
                                  x_min=self.x_min, x_max=self.x, y_min=self.y_min, y_max=self.y)
        self.upper_right = Segment(slope=-1, y_intercept=y-self.x_min+1,
                                   x_min=self.x, x_max=self.x_max, y_min=self.y, y_max=self.y_max)
        self.upper_left = Segment(slope=1, y_intercept=y+self.x_max+1,
                                  x_min=self.x_min, x_max=self.x, y_min=self.y, y_max=self.y_max)
        self.lower_right = Segment(slope=1, y_intercept=y-self.x_max-1,
                                   x_min=self.x, x_max=self.x_max, y_min=self.y_min, y_max=self.y)

    def __str__(self):
        return f'{self.__class__.__name__} ({self.x},{self.y}): {self.search_range}'

    def y_coverage(self, y: int):
        """Return the min and max x values covered by this sensor at row y"""
        r = self.search_range - abs(self.y - y)
        if r < 0:
            return None
        return self.x - r, self.x + r

    def no_overlap(self, other: 'Sensor'):
        """Returns True if the two sensors are guaranteed not to overlap, otherwise False"""
        return (self.x_min > other.x_max or other.x_min > self.x_max or
                self.y_min > other.y_max or other.y_min > self.y_max)

    def search_beacon_options(self, other: 'Sensor'):
        """Return possible locations for the missing beacon based on where sensor bounds intersect"""
        if self.no_overlap(other):
            return set()
        options = set()
        compare_segments = (
            (self.lower_left,  other.upper_right),
            (self.lower_left,  other.lower_right),
            (self.upper_right, other.upper_left),
            (self.upper_right, other.lower_right),
            (self.upper_left,  other.lower_left),
            (self.upper_left, other.upper_right),
            (self.lower_right, other.lower_left),
            (self.lower_right, other.upper_right)
        )
        for segment1, segment2 in compare_segments:
            options.update(segment1.intersections(segment2))
        return options


class Segment:
    def __init__(self, slope: int, y_intercept: int, x_min: int, x_max: int, y_min: int, y_max: int):
        # slope isn't used since in this case it's always 1 or -1. Included for debugging reasons though.
        self.slope = slope
        self.y_intercept = y_intercept
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def in_bounds(self, x: int, y: int):
        """Return True if point x,y is within the bounds of this line segment, otherwise False"""
        x_in_bounds = self.x_min <= x <= self.x_max
        y_in_bounds = self.y_min <= y <= self.y_max
        return x_in_bounds and y_in_bounds

    def intersections(self, other: 'Segment'):
        """Return points where the two line segments intersect"""
        if self.slope == -1:
            return (x for x in self._intersections(self.y_intercept, other.y_intercept) if self.in_bounds(*x))
        else:
            return (x for x in self._intersections(other.y_intercept, self.y_intercept) if self.in_bounds(*x))

    @staticmethod
    def _intersections(a: int, b: int):
        """
        Return the points where a line with slope -1 and y intercept "a" intersects with a line with slope 1 and
        y-intercept "b". Derived from the two equations y = -x + a and y = x + b.
        """
        diff = a - b
        if diff % 2 == 0:
            x = diff // 2
            yield x, x + b
        else:
            # I don't know if returning all 4 nearby points is necessary, but it doesn't really hurt so whatever.
            x = diff / 2
            y = x + b
            yield floor(x), floor(y)
            yield floor(x), ceil(y)
            yield ceil(x), floor(y)
            yield ceil(x), ceil(y)


def merge_ranges(ranges):
    range_iter = iter(sorted(ranges))
    rmin, rmax = next(range_iter)
    for next_min, next_max in range_iter:
        if next_min <= rmax:
            rmax = max(rmax, next_max)
        else:
            yield rmin, rmax
            rmin = next_min
            rmax = next_max
    yield rmin, rmax


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def parse_sensors(raw_input: str) -> list:
    sensors = list()
    for line in raw_input.splitlines():
        parts = line.split()
        sensor_x = int(parts[2][2:-1])
        sensor_y = int(parts[3][2:-1])
        beacon_x = int(parts[8][2:-1])
        beacon_y = int(parts[9][2:])
        d = distance(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(Sensor(sensor_x, sensor_y, d))
    return sensors


def solve(raw_input: str) -> tuple:
    sensors = parse_sensors(raw_input)
    a = solve_a(sensors)
    b = solve_b(sensors)
    return a, b


def solve_a(sensors) -> int:
    ranges = merge_ranges(c for c in [s.y_coverage(2000000) for s in sensors] if c is not None)
    return sum(b - a for a, b in ranges)


def solve_b(sensors, search_max=4000000) -> int:
    # corners need to be checked since they could be the answer without needing intersecting sensors.
    intersections = {(0, 0), (0, search_max), (search_max, 0), (search_max, search_max)}
    for s1, s2 in combinations(sensors, 2):
        intersections.update(s1.search_beacon_options(s2))
    for x, y in intersections:
        if not (0 <= x <= search_max and 0 <= y <= search_max):
            continue
        for sensor in sensors:
            if distance(sensor.x, sensor.y, x, y) <= sensor.search_range:
                break
        else:
            return (4000000 * x) + y


def main():
    with open('./day15_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B: {b}')
    print(f'Elapsed time: {elapsed_ms} ms')


if __name__ == '__main__':
    main()
