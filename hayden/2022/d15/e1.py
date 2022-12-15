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
        l_max = search(row, sensors, fixed_ents, left=True)
        r_max = search(row,  sensors, fixed_ents)
        print(r_max - l_max)


def search(row, sensors, fixed_ents, left=False):
    l_max = 0
    incr = 1
    skips = 0
    if left:
        incr = -1
    in_sight = True
    while in_sight:
        seen_once = False
        for sensor in sensors:
            if (row, l_max) in fixed_ents:
                print("skip it")
                skips += 1
                seen_once = True
                break
            if sensor.in_coverage((row, l_max)):
                seen_once = True
                break
        if not seen_once:
            in_sight = False
            break
        l_max += incr
    return l_max - skips

if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")