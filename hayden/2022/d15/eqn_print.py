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
    def print_eqn(self):
        print(f"abs(x-{self.x}) + abs(y+{self.y}) = {self.distance}")
        print(f"pos = x - {self.x} - {self.y}")
        print(f"neg = -x + {self.x} - {self.y}")
        print(f"plt = x - {self.x} - {self.y} + {self.distance}")
        print(f"prt = x - {self.x} - {self.y} - {self.distance}")
        print(f"nrt = -x + {self.x} - {self.y} + {self.distance}")
        print(f"nlt = -x + {self.x} - {self.y} - {self.distance}")
    def line_offs(self):
        # sensy + sensx + dist -> Neg
        # sensy + sensx - dist -> Neg
        # sensy - sensx + dist -> Pos
        # sensy - sensx - dist -> Pos
        return [\
            (-self.x-self.y+self.distance, -self.x-self.y-self.distance),\
            (+self.x-self.y+self.distance, +self.x-self.y-self.distance),\
        ]
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
        positive_lines = []
        negative_lines = []
        for locstr in locstrs:
            [s_x,s_y,b_x,b_y] = re.findall("(-?\d+)", locstr)
            senpoint = (int(s_x), int(s_y))
            beaconpt = (int(b_x), int(b_y))
            sensor = Sensor(sensor=senpoint, beacon=beaconpt)
            [posl, negl] = sensor.line_offs()
            positive_lines.append((senpoint, posl[0]))
            positive_lines.append((senpoint, posl[1]))
            negative_lines.append((senpoint, negl[0]))
            negative_lines.append((senpoint, negl[1]))
            sensors.append(sensor)
            fixed_ents.add(senpoint)
            fixed_ents.add(beaconpt)
        lines = set()
        for pos_line_1 in positive_lines:
            for pos_line_2 in positive_lines:
                dist = max(pos_line_1[1], pos_line_2[1]) - min(pos_line_1[1], pos_line_2[1]) 
                if dist == 3:
                    key = sorted([pos_line_1[0], pos_line_2[0]])
                    lines.add((key[0], key[1]))
        for neg_line_1 in negative_lines:
            for neg_line_2 in negative_lines:
                dist = max(neg_line_1[1], neg_line_2[1]) - min(neg_line_1[1], neg_line_2[1])
                if dist == 3:
                    key = sorted([neg_line_1[0], neg_line_2[0]])
                    key = (key[0], key[1])
                    if key in lines:
                        print(f"{neg_line_1[0]} and {neg_line_2[0]} MATCH")


if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")