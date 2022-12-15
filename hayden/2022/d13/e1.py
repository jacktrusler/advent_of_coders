from time import perf_counter
import queue
import json

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
            result = drain_loop(lhs, rhs);
            if result:
                sum_of_indices += indice
                
        print(sum_of_indices)


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



def parserino(line):
    return json.loads(line)
    
        



        

if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")