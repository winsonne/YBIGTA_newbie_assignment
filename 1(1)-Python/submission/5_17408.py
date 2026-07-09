from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    def __init__(
        self,
        data: list[T],
        default: U,
        f_conv: Callable[[T], U],
        f_merge: Callable[[U, U], U],
    ) -> None:
        self.n = len(data)
        self.default = default
        self.f_conv = f_conv
        self.f_merge = f_merge

        self.size = 1
        while self.size < self.n:
            self.size *= 2

        self.tree: list[U] = [self.default for _ in range(self.size * 2)]

        for i in range(self.n):
            self.tree[self.size + i] = self.f_conv(data[i])

        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.f_merge(self.tree[i * 2], self.tree[i * 2 + 1])

    def update(self, index: int, value: T) -> None:
        pos = self.size + index
        self.tree[pos] = self.f_conv(value)

        pos //= 2
        while pos >= 1:
            self.tree[pos] = self.f_merge(self.tree[pos * 2], self.tree[pos * 2 + 1])
            pos //= 2

    def query(self, left: int, right: int) -> U:
        left += self.size
        right += self.size

        left_result = self.default
        right_result = self.default

        while left <= right:
            if left % 2 == 1:
                left_result = self.f_merge(left_result, self.tree[left])
                left += 1

            if right % 2 == 0:
                right_result = self.f_merge(self.tree[right], right_result)
                right -= 1

            left //= 2
            right //= 2

        return self.f_merge(left_result, right_result)

    def find_kth(self, k: int) -> int:
        node = 1

        while node < self.size:
            left = node * 2
            left_value = self.tree[left]

            if not isinstance(left_value, int):
                raise TypeError("find_kth는 int 세그먼트 트리에서만 사용할 수 있습니다.")

            if left_value >= k:
                node = left
            else:
                k -= left_value
                node = left + 1

        return node - self.size


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    input = sys.stdin.readline

    n = int(input())
    numbers = list(map(int, input().split()))

    tree: SegmentTree[int, Pair] = SegmentTree(
        numbers,
        Pair.default(),
        Pair.f_conv,
        Pair.f_merge,
    )

    m = int(input())
    outputs: list[str] = []

    for _ in range(m):
        query = list(map(int, input().split()))

        if query[0] == 1:
            index = query[1] - 1
            value = query[2]
            tree.update(index, value)

        else:
            left = query[1] - 1
            right = query[2] - 1
            outputs.append(str(tree.query(left, right).sum()))

    print("\n".join(outputs))


if __name__ == "__main__":
    main()