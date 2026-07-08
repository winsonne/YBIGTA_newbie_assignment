from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        pointer = 0
        for element in seq:
            node = self[pointer]
            next_index: Optional[int] = None
            for child_index in node.children:
                if self[child_index].body == element:
                    next_index = child_index
                    break

            if next_index is None:
                self.append(TrieNode(body=element))
                next_index = len(self) - 1
                node.children.append(next_index)

            pointer = next_index

        self[pointer].is_end = True

    def find(self, seq: Iterable[T]) -> Optional[int]:
        """
        seq: T의 열

        returns: seq에 해당하는 노드의 인덱스. 존재하지 않으면 None.
        """
        pointer = 0
        for element in seq:
            node = self[pointer]
            next_index: Optional[int] = None
            for child_index in node.children:
                if self[child_index].body == element:
                    next_index = child_index
                    break
            if next_index is None:
                return None
            pointer = next_index
        return pointer


import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""

MOD = 1_000_000_007
def main() -> None:
    sys.setrecursionlimit(10000)

    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]

    fact: list[int] = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i - 1] * i) % MOD

    trie: Trie[int] = Trie()
    for name in names:
        trie.push(ord(c) - ord('A') for c in name)

    def dfs(index: int) -> int:
        """
        해당 노드를 루트로 하는 서브트리가 만들 수 있는 이름 배열 방법의 수를 반환한다.
        """
        node = trie[index]
        branch_count = len(node.children) + (1 if node.is_end else 0)
        result = fact[branch_count]
        for child_index in node.children:
            result = (result * dfs(child_index)) % MOD
        return result

    print(dfs(0) % MOD)


if __name__ == "__main__":
    main()