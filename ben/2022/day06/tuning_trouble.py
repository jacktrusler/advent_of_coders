import aoc


def find_marker(message: str, window: int) -> int:
    return next(i for i in range(window, len(message)) if len(set(message[i-window:i])) == window)

@aoc.register(__file__)
def answers():
    message = aoc.read_data()
    yield find_marker(message, window=4)
    yield find_marker(message, window=14)

if __name__ == '__main__':
    aoc.run()
