"""The Megaboy Destroyer"""

from collections import Counter

DISK_SPACE = 70000000
REQD_FREE = 30000000


def main():
    """Exercise 1"""
    ductr = Counter({"/": 0})
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_commands:
        f_drained = False
        output_buffer = []
        is_buffering = False
        working_dir = ["/"]
        while not f_drained:
            line = f_commands.readline()
            if not line:
                f_drained = True
                break
            if line[0] == "$":
                if is_buffering:
                    ls_handler(working_dir, output_buffer, ductr)
                    output_buffer = []
                    is_buffering = False
                command_args = line.split()
                if command_args[1] == "ls":
                    is_buffering = True
                if command_args[1] == "cd":
                    directory = command_args[2].strip()
                    if directory == "/":
                        working_dir = ["/"]
                    elif directory == "..":
                        working_dir.pop()
                    else:
                        working_dir.append(directory)
            else:
                if is_buffering:
                    output_buffer.append(line)
    f_commands.close()
    df = DISK_SPACE - ductr["/"]
    reqd_reclaim = REQD_FREE - df
    best_size = ductr["/"]
    best_delta = best_size - reqd_reclaim
    for _, du in ductr.items():
        candidate_size = du
        if candidate_size < reqd_reclaim:
            continue
        candidate_delta = candidate_size - reqd_reclaim
        if candidate_delta < best_delta:
            best_delta = candidate_delta
            best_size = candidate_size
    print(best_size)


def ls_handler(working_dir, output_buffer, ductr):
    """No Depth"""
    for outln in output_buffer:
        ls_out = outln.strip().split()
        if ls_out[0] == "dir":
            ins_dir = "/".join(working_dir) + ls_out[1]
            ductr.update({ins_dir: 0})
        else:
            ins_size = int(ls_out[0])
            breadcrumbs = working_dir.copy()
            for _ in range(len(breadcrumbs)):
                upd_dir = "/".join(breadcrumbs)
                ductr.update({upd_dir: ins_size})
                breadcrumbs.pop()
                

if __name__ == "__main__":
    main()
