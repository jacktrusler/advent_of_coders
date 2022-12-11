from time import perf_counter
LIT_PIXEL = "#"
UNLIT_PIXEL = "."
def main():
   with open(file="inputs.txt", mode="r", encoding="utf-8") as f_signals:
    cycles = 1
    x_reg = 1
    h_pos = 0

    def run_clock(ticks):
        nonlocal cycles
        nonlocal x_reg
        nonlocal h_pos
        for _ in range(ticks):
            if abs(x_reg-h_pos) <= 1:
                hsync(LIT_PIXEL)
            else: 
                hsync(UNLIT_PIXEL)
            h_pos+=1
            if cycles % 40 == 0:
                vsync()
                h_pos = 0
            cycles+=1
    
    def hsync(lit):
        print(lit,end="")
    def vsync():
        print()


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


        



if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")