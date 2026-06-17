from collections import defaultdict
from typing import Dict, Tuple, List


Permutation = Tuple[int, ...]


def identity_perm(n: int) -> Permutation:
    return tuple(range(1, n + 1))


def staircase_word(n: int) -> List[int]:
    """
    Return the staircase word.

    For S_6, this returns:
        [5, 4, 3, 2, 1,
         5, 4, 3, 2,
         5, 4, 3,
         5, 4,
         5]

    """
    word = []

    for row in range(1, n):
        # Row length is n - row.
        # Labels are row, row+1, ..., n-1.
        # We read right-to-left, so n-1, ..., row.
        for q in range(n - 1, row - 1, -1):
            word.append(q)

    return word


def right_multiply_simple_transposition(p: Permutation, q: int) -> Permutation:
    """
    Compute p * s_q.
    """
    p = list(p)
    p[q - 1], p[q] = p[q], p[q - 1]
    return tuple(p)


def count_total_pipe_dreams(target: List[int] | Permutation) -> int:
    """
    Count all ordinary not-necessarily-reduced pipe dreams for target.

    """
    target = tuple(target)
    n = len(target)

    dp: Dict[Permutation, int] = defaultdict(int)
    dp[identity_perm(n)] = 1

    for q in staircase_word(n):
        new_dp = dp.copy()

        for perm, count in dp.items():
            next_perm = right_multiply_simple_transposition(perm, q)
            new_dp[next_perm] += count

        dp = new_dp

    return dp[target]


def count_pipe_dreams_by_crosses(target: List[int] | Permutation) -> Dict[int, int]:
    """
    Count pipe dreams for target, grouped by number of crosses.

    Returns a dictionary:
        {number_of_crosses: count}
    """
    target = tuple(target)
    n = len(target)

    dp: Dict[Permutation, Dict[int, int]] = {
        identity_perm(n): {0: 1}
    }

    for q in staircase_word(n):
        new_dp: Dict[Permutation, Dict[int, int]] = {
            perm: counts.copy()
            for perm, counts in dp.items()
        }

        for perm, counts in dp.items():
            next_perm = right_multiply_simple_transposition(perm, q)

            if next_perm not in new_dp:
                new_dp[next_perm] = defaultdict(int)

            for crosses, count in counts.items():
                new_dp[next_perm][crosses + 1] = (
                    new_dp[next_perm].get(crosses + 1, 0) + count
                )

        dp = new_dp

    return dict(sorted(dp.get(target, {}).items()))


def inversion_length(p: List[int] | Permutation) -> int:
    """
    Number of inversions of a permutation.
    """
    p = tuple(p)
    inv = 0

    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1

    return inv


if __name__ == "__main__":
    w = (1, 2, 3, 4, 5, 6,7,8,9,10)

    print("total:", count_total_pipe_dreams(w))