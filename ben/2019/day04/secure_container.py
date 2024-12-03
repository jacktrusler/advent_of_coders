import aoc


def increasing(digit: str):
    return all(x <= y for x, y in tuple(zip(digit, digit[1:])))
    
def has_pair(digit: str):
    return any(x == y for x, y in tuple(zip(digit, digit[1:])))
    
def has_exclusive_pair(digit: str):
    _digit = f'x{digit}x'
    quads = tuple(zip(_digit, _digit[1:], _digit[2:], _digit[3:]))
    return any(a != b and b == c and c != d for a, b, c, d in reversed(quads))

@aoc.register(__file__)
def answers():
    pw_low, pw_high = map(int, aoc.read_data().split('-'))

    valid_passwords = {x for x in range(pw_low, pw_high + 1) if increasing(str(x))}
    valid_passwords = {x for x in valid_passwords if has_pair(str(x))}
    yield len(valid_passwords)

    valid_passwords = {x for x in valid_passwords if has_exclusive_pair((str(x)))}
    yield len(valid_passwords)

if __name__ == '__main__':
    aoc.run()
