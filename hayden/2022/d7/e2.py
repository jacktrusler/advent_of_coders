"""No Space Left On Device"""

from collections import Counter

DISK_SPACE = 70000000
REQD_FREE = 30000000

class Directory:
    def __init__(self, name, parent):
        self.parent = parent
        self.children = dict()
        self.name = name

    def size(self):
        """sneaky recursion"""
        dir_total = 0
        for _, child in self.children.items():
            dir_total += child.size()
        return dir_total

    def fqpath(self):
        """more sneaky recurison?"""
        path = self.name
        if self.parent:
            return self.parent.fqpath() + "/" + path
        else:
            return ""
    parent: None
    children: None
    name: None


class File:
    def __init__(self, name, size, parent):
        self.parent = parent
        self.name = name
        self._size = size

    def size(self):
        """files just return their size"""
        return self._size

    def fqpath(self):
        """same sneaky recursion :o"""
        path = self.name
        return self.parent.fqpath() + "/" + path

    parent: None
    name: None
    _size: None


def main():
    """Exercise 1"""
    root = Directory("/", None)
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_commands:
        commands = f_commands.readlines()
        f_commands.close()
        output_buffer = []
        buffering_output = False
        dir_context = None
        for line in commands:
            if line[0] == "$":
                if buffering_output:
                    ls_handler(dir_context, output_buffer)
                    output_buffer = []
                    buffering_output = False
                command_args = line.split()
                if command_args[1] == "ls":
                    buffering_output = True
                if command_args[1] == "cd":
                    dir_tree = command_args[2].strip()
                    if dir_tree == "/":
                        dir_context = root
                    elif dir_tree == "..":
                        dir_context = dir_context.parent
                    else:
                        dir_context = dir_context.children[dir_tree]
            else:
                if buffering_output:
                    output_buffer.append(line)
        ductr = Counter()
        ductr.update({"/": root.size()})
        calc_du(root.children, ductr)
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
            

        
def calc_du(dir_contents, ductr):
    """wow I hope this doesn't blow up my proc"""
    for _, dir_entry in dir_contents.items():
        if isinstance(dir_entry, Directory):
            dir_path = dir_entry.fqpath()
            dir_size = dir_entry.size()
            ductr.update({dir_path: dir_size})
            calc_du(dir_entry.children, ductr)
        

def ls_handler(dir_context, output_buffer):
    """Handle LS output"""
    for outln in output_buffer:
        ls_out = outln.strip().split()
        if ls_out[0] == "dir":
            ins_dir = Directory(ls_out[1], dir_context)
            dir_context.children[ls_out[1]] = ins_dir
        else:
            ins_file = File(ls_out[1], int(ls_out[0]), dir_context)
            dir_context.children[ls_out[1]] = ins_file


if __name__ == "__main__":
    main()
