import aoc
import math


# Baby-step Giant-step algorithm
def bsgs(base, pubkey, modulo) -> int | None:
    m = math.ceil(math.sqrt(modulo))
    table = {pow(base, i, modulo): i for i in range(m)}
    inv = pow(base, -m, modulo)
    
    for i in range(m):
        y = (pubkey * pow(inv, i, modulo)) % modulo
        if y in table:
            return i * m + table[y]
    return None


@aoc.register(__file__)
def answers():
    INITIAL_SUBJECT = 7
    MOD_NO = 20201227

    card_pubkey, door_pubkey = map(int, aoc.read_lines())
    door_loop = bsgs(INITIAL_SUBJECT, door_pubkey, MOD_NO)
    encryption_key = pow(card_pubkey, door_loop, MOD_NO)
    yield encryption_key

if __name__ == '__main__':
    aoc.run()
