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