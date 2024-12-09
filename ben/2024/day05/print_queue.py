import aoc
from collections import defaultdict, deque, namedtuple


RULES = defaultdict(set)
UpdateOrderResult = namedtuple('UpdateOrderResult', ['middle_number', 'fix_made'])

def order(update: tuple[int]) -> UpdateOrderResult:
    queue = deque(update)
    fix_made = False
    order = []

    while queue:
        page = queue.popleft()
        if RULES[page] & set(queue):
            queue.append(page)
            fix_made = True
            continue
        order.append(page)

    middle_idx = int((len(order) - 1) / 2)
    return UpdateOrderResult(order[middle_idx], fix_made)

@aoc.register(__file__)
def answers():
    rules, updates = aoc.read_chunks()
    for rule in rules.splitlines():
        first, second = rule.split('|')
        RULES[int(second)].add(int(first))
    updates = tuple(tuple(map(int, u.split(','))) for u in updates.splitlines())
    
    reuslts = tuple(order(u) for u in updates)
    yield sum(x.middle_number for x in reuslts if not x.fix_made)
    yield sum(x.middle_number for x in reuslts if x.fix_made)

if __name__ == '__main__':
    aoc.run()
