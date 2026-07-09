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
from typing import Optional

"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index: Optional[int] = None
        for child_index in trie[pointer].children:
            if trie[child_index].body == element:
                new_index = child_index
                break

        assert new_index is not None

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    results = []

    while idx < len(data):
        n = int(data[idx])
        idx += 1
        words = data[idx:idx + n]
        idx += n

        trie: Trie[str] = Trie()
        for word in words:
            trie.push(word)

        total = sum(count(trie, word) for word in words)
        results.append(f"{total / n:.2f}")

    print('\n'.join(results))


if __name__ == "__main__":
    main()