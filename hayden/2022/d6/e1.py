"""Parse elf packets"""

from collections import deque

END_SEQUENCE_LEN = 4


def main():
    """AoC Runner"""
    with open(file="input.txt", mode="r", encoding="utf-8") as f_data_stream:
        packets = []
        current_packet = []
        current_packet_readb4 = 0
        trailer_queue = deque()
        drained_data = False
        while not drained_data:
            ds_next = f_data_stream.read(1)
            current_packet_readb4 += 1
            if not ds_next:
                drained_data = True
                current_packet.extend(trailer_queue)
                packets.append(current_packet)
                current_packet = []
                break
            if len(trailer_queue) == END_SEQUENCE_LEN:
                current_packet.append(trailer_queue.popleft())
            trailer_queue.append(ds_next)
            trailer_uniq = set(trailer_queue)
            if len(trailer_uniq) == END_SEQUENCE_LEN:
                print("End of Packet read after ", current_packet_readb4)
                packets.append(current_packet)
                trailer_queue = deque()
                current_packet = []


if __name__ == "__main__":
    main()
