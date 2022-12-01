from __future__ import annotations
import aoc
from dataclasses import dataclass, field
from math import prod
import numpy as np
import re


@dataclass
class Field:
    name: str
    values: set[int] = field(default_factory=set, repr=False)
    idx: int = field(default=-1, init=False, repr=False)

    def __hash__(self):
        return hash(self.name)

    def match(self, other: set[int]) -> bool:
        return other <= self.values

    @staticmethod
    def from_string(field_str: str) -> Field:
        data = re.match(r'(?P<name>.*): (?P<min_a>.*)-(?P<max_a>.*) or (?P<min_b>.*)-(?P<max_b>.*)', field_str).groupdict()
        set_a = set(range(int(data['min_a']), int(data['max_a']) + 1))
        set_b = set(range(int(data['min_b']), int(data['max_b']) + 1))
        return Field(name=data['name'], values=set_a | set_b)

class Ticket:
    def __init__(self, values: list[int]):
        self.values = values

    def error_rate(self, valid_values: set[int]) -> int:
        return sum(x for x in self.values if x not in valid_values)

    @staticmethod
    def from_string(ticket_str: str) -> Ticket:
        return Ticket(list(map(int, ticket_str.split(','))))
        

def match_fields(tickets: list[Ticket], fields: list[Field]) -> list[Field]:
    value_grid = np.array([t.values for t in tickets]).T
    ticket_fields = {idx: set(x) for idx, x in enumerate(value_grid)}
    match_dict = {f: {idx for idx, x in ticket_fields.items() if f.match(x)} for f in fields}

    while match_dict:
        matchable = next(f for f, matches in match_dict.items() if len(matches) == 1)
        matchable.idx = next(iter(match_dict.pop(matchable)))
        match_dict = {f: matches - {matchable.idx} for f, matches in match_dict.items()}
    return fields


@aoc.register(__file__)
def answers():
    fields, my_ticket, tickets = aoc.read_chunks()

    fields = [Field.from_string(f) for f in fields.splitlines()]
    my_ticket = Ticket.from_string(my_ticket.splitlines()[1])
    tickets = [Ticket.from_string(t) for t in tickets.splitlines()[1:]]

    valid_values = set.union(*[x.values for x in fields])
    yield sum(t.error_rate(valid_values) for t in tickets)

    valid_tickets = [t for t in tickets if t.error_rate(valid_values) == 0]
    fields = match_fields(valid_tickets, fields)
    
    departure_fields = [f for f in fields if f.name.startswith('departure')]
    departure_values = [my_ticket.values[f.idx] for f in departure_fields]
    yield prod(departure_values)

if __name__ == '__main__':
    aoc.run()
