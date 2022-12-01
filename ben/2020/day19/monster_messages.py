from __future__ import annotations
import aoc
from dataclasses import dataclass, field
import re


@dataclass
class Rule:
    id: int
    letter: str = field(default=None, repr=False)
    rule_sets: list = field(default_factory = list, repr=False)

    def matches(self, rules: dict[int, Rule], message: str, idx: int = 0) -> list[int]:
        if idx >= len(message):
            return []
        if self.letter is not None:
            return [idx + 1] if message[idx] == self.letter else []

        retval = []
        for option in self.rule_sets:
            option_matches = [idx]
            
            for rule_id in option:
                rule = rules[rule_id]

                rule_matches = []
                for i in option_matches:
                    rule_matches += rule.matches(rules, message, i)
                option_matches = rule_matches

            retval += option_matches
        return retval

    def match(self, rules: dict[int, Rule], message: str) -> bool:
        return len(message) in self.matches(rules, message)

    @staticmethod
    def from_string(rule_str: str) -> Rule:
        rule_id, rule_str = rule_str.split(':')
        rule_id = int(rule_id)
        rule_sets = rule_str.strip()

        m = re.match(r'\"(?P<letter>[a-z])\"', rule_sets)
        if m is not None:
            return Rule(rule_id, letter=m.group('letter'))
            
        rule_sets = [tuple([int(x) for x in option.strip().split(' ')]) for option in rule_str.split('|')]
        return Rule(rule_id, rule_sets=rule_sets)


@aoc.register(__file__)
def answers():
    rules, messages = aoc.read_chunks('data')
    rules = [Rule.from_string(line) for line in rules.split('\n')]
    rules = {rule.id: rule for rule in rules}
    messages = messages.split('\n')

    valid_messages = [msg for msg in messages if rules[0].match(rules, msg)]
    yield len(valid_messages)

    rules[8] = Rule.from_string('8: 42 | 42 8')
    rules[11] = Rule.from_string('11: 42 31 | 42 11 31')
    valid_messages = [msg for msg in messages if rules[0].match(rules, msg)]
    yield len(valid_messages)

if __name__ == '__main__':
    aoc.run()
