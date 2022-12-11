from time import perf_counter
def main():
   with open(file="inputs.txt", mode="r", encoding="utf-8") as f_signals:
    cycles = 1
    sig_sum = 0
    x_reg = 1

    def run_clock(ticks):
        nonlocal cycles
        nonlocal sig_sum
        nonlocal x_reg
        for _ in range(ticks):
            if cycles == 20 or (cycles - 20) % 40 == 0:
                sig_sum += x_reg * cycles
                print(f"{cycles} x_reg {x_reg} {x_reg * cycles}")
            cycles+=1

    while True:
        instruction = f_signals.readline()
        if not instruction:
            break
        if instruction[0] == "n":
            run_clock(1)
        elif instruction[0] == "a":
            run_clock(2)
            x_acc = int(instruction[5:].strip())
            x_reg += x_acc
    f_signals.close()
    print(sig_sum)


        



if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")