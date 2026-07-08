from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    input = sys.stdin.readline
    t = int(input())
    outputs: list[str] = []

    for _ in range(t):
        n, m = map(int, input().split())
        movies = list(map(int, input().split()))

        size = n + m + 1
        data = [0] * size
        position = [0] * (n + 1)

        for movie in range(1, n + 1):
            position[movie] = m + movie
            data[m + movie] = 1

        tree: SegmentTree[int, int] = SegmentTree(
            data,
            0,
            lambda x: x,
            lambda a, b: a + b,
        )

        top = m
        result: list[str] = []

        for movie in movies:
            pos = position[movie]
            result.append(str(tree.query(0, pos - 1)))

            tree.update(pos, 0)
            tree.update(top, 1)

            position[movie] = top
            top -= 1

        outputs.append(" ".join(result))

    print("\n".join(outputs))


if __name__ == "__main__":
    main()