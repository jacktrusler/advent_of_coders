from __future__ import annotations
from abc import ABC, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import Any, ClassVar
from uuid import uuid4, UUID


@dataclass()
class PathNode(ABC):
    distance: int = field(frozen=True)
    uid: UUID = field(default_factory=lambda: uuid4())

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other: PathNode):
        return self.uid == other.uid

    @classmethod
    def new(cls, prev: PathNode) -> PathNode:
        return cls(distance=prev.distance+1)

    @abstractmethod
    def adjacent(self) -> set[PathNode]:
        pass

    @abstractmethod
    def cost(self, other: PathNode) -> int:
        pass

    def can_move_to(self, other: PathNode, visited: set[PathNode]) -> bool:
        return other not in visited

    def path_to(self, end: int | PathNode) -> int | None:
        queue = deque([self])
        visited = set()

        while queue:
            node = queue.pop()

            if node == end:
                return node.distance
            if node.uid in visited:
                continue
            visited.add(node.uid)

            for adj in node.adjacent() - visited:
                if not node.can_move_to(other=adj, visited=visited):
                    continue
                queue.append(__class__.new(node, adj))
        return None
