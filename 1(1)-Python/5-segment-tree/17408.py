from __future__ import annotations
from lib import SegmentTree
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