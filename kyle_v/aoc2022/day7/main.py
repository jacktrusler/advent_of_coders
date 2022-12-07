from anytree import Node, RenderTree

root = Node('/',size=-1,is_dir=True)

def add_command(command,current_node):
    if command[:4] == '$ cd':
        dir = command[4:].strip()

        if dir == '..':
            
            dir_size = 0

            # add child directory sizes to the files found in this directory already
            for _,_,child in RenderTree(current_node):
                if child.parent == current_node:
                    dir_size = dir_size + child.size
            current_node.size = dir_size

            current_node = current_node.parent
        else:
            moving_to_dir = Node(dir, size=-1,is_dir=True,parent=current_node)
            current_node = moving_to_dir
        # print(f'cd command found to move to dir {dir}')
    elif command[:4] == '$ ls':
        # print('list command found')
        pass
    elif command[:3] == 'dir':
        # print('directory found')
        pass
    else:
        filename = command.split()[1]
        filesize = int(command.split()[0])
        # print(f'file {filename} found of size {filesize}!')
        # insert node into tree
        Node(filename,size=filesize,is_dir=False,parent=current_node)
    return current_node

def part_1(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        
        # execute commands
        current_node = root
        for command in lines:
            current_node = add_command(command,current_node)

        # add calculate total sizes moving up the directory tree
        while(current_node.parent is not root):
            current_node = add_command('$ cd ..',current_node)
        add_command('$ cd ..',current_node)

        # print out tree for fun to see what it looks like
        for pre, fill, node in RenderTree(root):
            print(pre, node.name, node.size)

        total = 0

        # add totals together
        for _,_,node in RenderTree(root):
            if node.is_dir and node.size < 100000 and node.name != '/':
                print(f'{node.name} fits the bill at size {node.size}!')
                total = total + node.size            

        print('total: ',total)

    return total

def part_2(input_file):
    with open(input_file) as f:
        lines = [line for line in f]

        # execute commands
        current_node = root
        for command in lines:
            current_node = add_command(command,current_node)

        # add calculate total sizes moving up the directory tree
        while(current_node.parent is not root):
            current_node = add_command('$ cd ..',current_node)
        add_command('$ cd ..',current_node)

        # print out tree for fun to see what it looks like
        # for pre, fill, node in RenderTree(root):
        #     print(pre, node.name, node.size)

        total_space = 70000000
        unused_space = -1
        additional_space_needed = -1

        for _,_,node in RenderTree(root):
            if node.is_dir and node.name == '/' and node.size != -1:
                unused_space = total_space - node.size
                additional_space_needed = 30000000 - unused_space
                print(f'unused space: {unused_space}')
                print(f'additional space needed: {additional_space_needed}')

        big_enough_dirs = []
        for _,_,node in RenderTree(root):
            if node.is_dir and node.name != '/' and node.size >= additional_space_needed:
                big_enough_dirs.append(node.size)

        print(min(big_enough_dirs))
        
    return min(big_enough_dirs)

if __name__ == '__main__':
    print('part 1 answer: ', part_1('testinput.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    