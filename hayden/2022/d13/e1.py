from time import perf_counter

def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_data:
        

if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")