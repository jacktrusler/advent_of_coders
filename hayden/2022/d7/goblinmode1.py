"""The Megaboy Destroyer"""

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
            if line[0] == "$":
                if line[2] == "l":
                    continue
                elif line[5] == "/":
                    inode_chain = [0]
                elif line[5] == ".":
                    inode_chain.pop()
                else:
                    inode_chain.append(next_inode)
                    ductr.insert(next_inode, 0)
                    next_inode+=1
            else:
                if line[0] == "d":
                    continue
                fsize = int(line.split()[0])
                for inode in inode_chain:
                    ductr[inode] += fsize
    underhundk = 0
    for inode_size in ductr:
        if inode_size <= 100000:
            underhundk += inode_size
    print(underhundk)

if __name__ == "__main__":
    main()
