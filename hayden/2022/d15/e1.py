from time import perf_counter
import numpy as np
import re

def manhattan(point1, point2):
    (x1, y1) = point1
    (x2, y2) = point2
    return abs(x2-x1) + abs(y2-y1)

class Sensor:
    def __init__(self, sensor, beacon) -> None:
        (self.x, self.y) = sensor
        self.pos = sensor
        self.distance = manhattan(sensor, beacon)
    def in_coverage(self, point):
        return manhattan(self.pos, point) <= self.distance
    def intersection_on(self, y):
        intersection = set()
        if y <= self.y + self.distance and y >= self.y - self.distance:
            d_2_g = self.distance - manhattan(self.pos, (self.x, y))
            intersection.add((self.x, y))
            while d_2_g > 0:
                intersection.add((self.x+d_2_g, y))
                intersection.add((self.x-d_2_g, y))
                d_2_g-=1
        return intersection

def main():
    with open("inputs.txt", mode="r", encoding='UTF8') as f_locations:
        locstrs = f_locations.readlines()
        f_locations.close()
        sensors = []
        fixed_ents = set()
        for locstr in locstrs:
            [s_x,s_y,b_x,b_y] = re.findall("(-?\d+)", locstr)
            senpoint = (int(s_x), int(s_y))
            beaconpt = (int(b_x), int(b_y))
            sensor = Sensor(sensor=senpoint, beacon=beaconpt)
            sensors.append(sensor)
            fixed_ents.add(senpoint)
            fixed_ents.add(beaconpt)
        row = 2000000
        intersections = set()
        for sensor in sensors:
            intersections = intersections.union(sensor.intersection_on(row))
        # Get left half to remove fixed ents

        print(len(intersections.difference(fixed_ents)))


if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")