from time import perf_counter
import queue
import re

def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_data:
        all_pairs = f_data.read().split("\n\n")
        sum_of_indices = 0
        indice = 0
        for pair in all_pairs:
            indice += 1
            [top, bottom] = pair.split("\n")
            lhs = parserino(top)
            rhs = parserino(bottom)
            print(f"Pair {indice}")
            if drain_loop(lhs, rhs):
                print("In Order")
                sum_of_indices += indice
            else:
                print("Not in order")
        print(sum_of_indices)


def drain_loop(lhs, rhs):
    l_test = None
    r_test = None
    while (not lhs.empty() or l_test is not None) and (not rhs.empty() or r_test is not None):
        if not l_test:
            l_test = lhs.get()
        if not r_test:
            r_test = rhs.get()
        print(f"Comparing {l_test} to {r_test}")
        jump_to_head = False
        if l_test == "noop":
            l_test = None
            jump_to_head = True
        if r_test == "noop":
            r_test = None
            jump_to_head = True
        if jump_to_head:
            print("Jumping to head because of no-op")
            continue
        determined = None
        if (l_test < r_test):
            print("Left less than Right, in order")
            determined = True
        if (l_test > r_test):
            print("Left larger tahn Right, incorrect")
            determined = False
        l_test = None
        r_test = None
        if determined is not None:
            return determined
    if rhs.empty():
        return False
    return True



def parserino(line):
    the_q = queue.Queue()
    matches = re.findall("(\d|\[)",line)
    for match in matches:
        if match == "[":
            the_q.put("noop")
        else:
            the_q.put(int(match))
    return the_q
    
        



        

if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")