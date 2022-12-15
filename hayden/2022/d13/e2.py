import copy
from functools import total_ordering
from time import perf_counter
import json

def drain_loop(lhs, rhs):
    while len(lhs) != 0 and len(rhs) != 0:
        result = None
        l_test = lhs.pop(0)
        r_test = rhs.pop(0)
        if isinstance(l_test, list) and not isinstance(r_test,list):
            r_test = [r_test]
            result = drain_loop(l_test, r_test)
        elif isinstance(r_test, list) and not isinstance(l_test,list):
            l_test = [l_test]
            result = drain_loop(l_test, r_test)
        elif isinstance(l_test,list) and isinstance(r_test, list):
            result = drain_loop(l_test, r_test)
        elif l_test > r_test:
            result = False
        elif l_test < r_test:
            result = True
        if result is not None:
            return result
    if len(rhs) < len(lhs):
        return False
    if len(lhs) < len(rhs):
        return True
    return None


@total_ordering
class Packet:
    def __init__(self, contents):
        self.contents = contents
    def __eq__(self, compared):
        result = drain_loop(copy.deepcopy(self.contents), copy.deepcopy(compared.contents))
        if result is None:
            return True
        else:
            return False
    def __lt__(self, compared):
        result = drain_loop(copy.deepcopy(self.contents), copy.deepcopy(compared.contents))
        if result is True:
            return True
        else:
            return False

def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_data:
        all_pairs = f_data.read().split("\n\n")
        indice = 0
        two_sep = Packet([[2]])
        six_sep = Packet([[6]])
        Packets = [Packet([[2]]),Packet([[6]])]
        for pair in all_pairs:
            [top, bottom] = pair.split("\n")
            lhs = parserino(top)
            rhs = parserino(bottom)
            Packets.append(lhs)
            Packets.append(rhs)
        sorted_Packets = sorted(Packets)
        two_ind = 0
        six_ind = 0
        for packet in sorted_Packets:
            indice += 1
            if two_ind == 0:
                if packet == two_sep:
                    two_ind = indice
            if two_ind != 0:
                if packet == six_sep:
                    six_ind = indice
                    break
        print(two_ind * six_ind)

def parserino(line):
    return Packet(json.loads(line))
    
if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")