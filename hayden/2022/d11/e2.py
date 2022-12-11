from time import perf_counter
import numpy as np

MAX_ROUNDS = 10000
INNER_CALM = 1
MAX_HEADROOM = 1

class Monkey:
    def __init__(self, monkey_block, gang):
        self.gang = gang
        self.inspections = 0
        monkey_block = monkey_block.split("\n")
        # Fill Pouch
        start_items_str = monkey_block[1][18:].split(',')
        self.pouch = np.empty(len(start_items_str),dtype=np.int64)
        for idx, item in enumerate(start_items_str):
            self.pouch[idx] = int(item)
        # Worry Parsing
        operation = monkey_block[2][23]
        rhs = monkey_block[2][25:]
        if rhs == "old":
            self.w_rhs = 2
            self.w_operation = "**"
            self.worry_mod = self.w_square
        else:
            self.w_rhs = int(rhs)
            if operation == "*":
                self.worry_mod = self.w_mul
            elif operation == "+":
                self.worry_mod = self.w_plus
        # Test Condition Parse
        modulo_str = monkey_block[3][21:]
        self.t_modulo = int(modulo_str)
        
        # Toss Outcomes
        t_str = monkey_block[4][29:]
        f_str = monkey_block[5][30:]
        self.t_cond = int(t_str)
        self.f_cond = int(f_str)
 
    def inspect(self):
        for idx, item in enumerate(self.pouch):
            self.pouch[idx] = (self.worry_mod(item) // INNER_CALM) % MAX_HEADROOM
            self.inspections += 1

    def toss(self):
        for item in self.pouch:
            if item % self.t_modulo == 0:
                self.gang[self.t_cond].catch(item)
            else:
                self.gang[self.f_cond].catch(item)
        self.pouch = np.empty(0,dtype=np.int64)

    def catch(self, item):
        self.pouch = np.append(self.pouch, item)

    def w_square (self, item):
        return item ** self.w_rhs
    
    def w_plus (self, item):
        return item + self.w_rhs

    def w_mul (self, item):
        return item * self.w_rhs
    max_headroom = 1
        
def main():
   with open(file="inputs.txt", mode="r", encoding="utf-8") as f_monkeys:
    global MAX_HEADROOM
    unparsed_monkeys= f_monkeys.read().split("\n\n")
    f_monkeys.close()
    monkeys = []
    #initialize monkeys
    multiples = set()
    for u_monkey in unparsed_monkeys:
        new_monkey = Monkey(u_monkey, monkeys)
        monkeys.append(new_monkey)
        multiples.add(new_monkey.t_modulo)
    for multiple in multiples:
        MAX_HEADROOM *= multiple
    # lets play
    for round in range(MAX_ROUNDS):
        for monkey in monkeys:
            monkey.inspect()
            monkey.toss()
    # Lets tally 
    monkeys.sort(reverse=True, key=lambda monkey: monkey.inspections)
    monkey_score = 1
    for m_id in range(2):
        monkey_score *= monkeys[m_id].inspections
    print(monkey_score)
    

    
if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")