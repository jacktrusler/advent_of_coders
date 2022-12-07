"""The Megaboy Destroyer"""

DISK_SPACE = 1300000000000
REQD_FREE = 300000000000

from array import array

def main():
    """Exercise 1"""
    next_inode = 1
    ductr = array('l')
    ductr.insert(0, 0)
    with open(file="7_megaboy.txt", mode="r", encoding="utf-8") as f_commands:
        #Read all lines in at once
        commands = f_commands.readlines()
        inode_chain = [0]
        for line in commands:
            #Is this a "Shell Line"
            if line[0:4] == "$ cd":
                directory = line[5:].strip()
                if directory == "/":
                    inode_chain = [0]
                elif directory == "..":
                    inode_chain.pop()
                else:
                    inode_chain.append(next_inode)
                    ductr.insert(next_inode, 0)
                    next_inode+=1
            else:
                if line[0] == "d" or line[0] == "$":
                    continue
                fsize = int(line.split()[0])
                for inode in inode_chain:
                    ductr[inode] += fsize
    df = DISK_SPACE - ductr[0]
    reqd_reclaim = REQD_FREE - df
    best_size = ductr[0]
    best_delta = best_size - reqd_reclaim
    for i in range(1,len(ductr)):
        candidate_size = ductr[i]
        if candidate_size < reqd_reclaim or candidate_size > best_size:
            continue
        candidate_delta = candidate_size - reqd_reclaim
        if candidate_delta < best_delta:
            best_delta = candidate_delta
            best_size = candidate_size
    print(best_size)

if __name__ == "__main__":
    main()
