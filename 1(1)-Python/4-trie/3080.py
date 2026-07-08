from lib import Trie
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