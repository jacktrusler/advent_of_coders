from __future__ import annotations
import aoc
from collections import defaultdict


Path = tuple[str]
PathTree = dict[Path, list]

def cd(paths: PathTree, cwd: Path, folder: str) -> Path:
    if folder == '..': return cwd[:-1]
    if folder == '/': return Path()

    new_folder = cwd + (folder,)
    paths[cwd].append(new_folder)
    return new_folder

def ls(paths: PathTree, cwd: Path, lines: str) -> Path:
    for line in lines:
        a, _ = line.split()
        if 'dir' not in a:
            paths[cwd].append(int(a))
    return cwd

def build_tree(commands: list[str]) -> PathTree:
    paths = defaultdict(list)
    cwd = tuple()
    for cmd in commands:
        if cmd.startswith('cd'):
            cwd = cd(paths, cwd, cmd.split()[-1])
        elif cmd.startswith('ls'):
            cwd = ls(paths, cwd, cmd.splitlines()[1:])
    return paths

def size_report(paths: PathTree, folder: Path) -> int:
    retval = 0
    for child in paths[folder]:
        if isinstance(child, int):
            retval += child
        else:
            retval += size_report(paths, child)
    return retval


@aoc.register(__file__)
def answers():
    commands = aoc.read_data().split('$ ')
    path_tree = build_tree(commands)

    sizes = {folder: size_report(path_tree, folder) for folder in path_tree.keys()}
    yield sum(x for x in sizes.values() if x <= 100_000)

    needed_space = 30_000_000 - (70_000_000 - sizes[Path()])
    yield min(x for x in sizes.values() if x >= needed_space)

if __name__ == '__main__':
    aoc.run()
