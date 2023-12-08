from __future__ import annotations
from typing import Any, Generator, Self


class TreeNode:
    def __init__(self, value: Any, parent: TreeNode = None):
        self.value = value
        self.parent = parent
        self.children = set()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value})'

    def parents(self) -> Generator[TreeNode]:
        level = self
        while (level := level.parent) is not None:
            yield level

    @property
    def top(self) -> TreeNode:
        *_, last = self.parents()
        return last
    
    def add_child(self, node: TreeNode) -> Self:
        node.parent = self
        self.children.add(node)
        return self
    
    def create_child(self, value: Any) -> TreeNode:
        child = TreeNode(value=value, parent=self)
        self.children.add(child)
        return child
    

if __name__ == '__main__':
    top = TreeNode(1)
    for x in range(2, 10):
        top.create_child(x)
    print(top)

