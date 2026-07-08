from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    input = sys.stdin.readline
    n = int(input())

    max_taste = 1_000_000
    data = [0] * (max_taste + 1)

    tree: SegmentTree[int, int] = SegmentTree(
        data,
        0,
        lambda x: x,
        lambda a, b: a + b,
    )

    outputs: list[str] = []

    for _ in range(n):
        query = list(map(int, input().split()))

        if query[0] == 1:
            rank = query[1]
            taste = tree.find_kth(rank)
            outputs.append(str(taste))

            current = tree.query(taste, taste)
            tree.update(taste, current - 1)

        else:
            taste = query[1]
            count = query[2]
            current = tree.query(taste, taste)
            tree.update(taste, current + count)

    print("\n".join(outputs))


if __name__ == "__main__":
    main()