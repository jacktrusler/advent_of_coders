from time import perf_counter
MAX_ROUNDS = 20

class Monkey:
    def __init__(self, monkey_block, gang):
        self.gang = gang
        self.inspections = 0
        monkey_block = monkey_block.split("\n")
        # Fill Pouch
        self.pouch = list()
        start_items_str = monkey_block[1][18:].split(',')
        for item in start_items_str:
            self.pouch.append(int(item))
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
        # Fail toss
        t_str = monkey_block[4][29:]
        f_str = monkey_block[5][30:]
        self.t_cond = int(t_str)
        self.f_cond = int(f_str)
 
    def inspect(self):
        mod_pouch = list()
        for item in self.pouch:
            mod_pouch.append(self.worry_mod(item) // 3)
            self.inspections += 1
        self.pouch = mod_pouch

    def toss(self):
        while True:
            if len(self.pouch) == 0:
                break
            item = self.pouch.pop(0)
            if item % self.t_modulo == 0:
                self.gang[self.t_cond].catch(item)
            else:
                self.gang[self.f_cond].catch(item)

    def catch(self, item):
        self.pouch.append(item)

    def w_square (self, item):
        return item ** self.w_rhs
    
    def w_plus (self, item):
        return item + self.w_rhs

    def w_mul (self, item):
        return item * self.w_rhs
        
def main():
   with open(file="inputs.txt", mode="r", encoding="utf-8") as f_monkeys:
    unparsed_monkeys= f_monkeys.read().split("\n\n")
    f_monkeys.close()
    monkeys = []
    #initialize monkeys
    for u_monkey in unparsed_monkeys:
        # print(u_monkey)
        monkeys.append(Monkey(u_monkey, monkeys))
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