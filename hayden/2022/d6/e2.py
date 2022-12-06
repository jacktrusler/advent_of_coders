"""Parse elf packets"""

from collections import deque

END_SEQUENCE_LEN = 14


def main():
    """AoC Runner"""
    with open(file="input.txt", mode="r", encoding="utf-8") as f_data_stream:
        messages = []
        current_message = []
        current_message_readb4 = 0
        trailer_queue = deque()
        drained_data = False
        while not drained_data:
            ds_next = f_data_stream.read(1)
            current_message_readb4 += 1
            if not ds_next:
                drained_data = True
                current_message.extend(trailer_queue)
                messages.append(current_message)
                current_message = []
                break
            if len(trailer_queue) == END_SEQUENCE_LEN:
                current_message.append(trailer_queue.popleft())
            trailer_queue.append(ds_next)
            trailer_uniq = set(trailer_queue)
            if len(trailer_uniq) == END_SEQUENCE_LEN:
                print("Start of Message read after ", current_message_readb4)
                messages.append(current_message)
                trailer_queue = deque()
                current_message = []


if __name__ == "__main__":
    main()
