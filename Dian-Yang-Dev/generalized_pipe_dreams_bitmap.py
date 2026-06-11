"""
generalized_pipe_dreams_bitmap.py

Generalized / not-necessarily-reduced pipe dreams using a bitmap representation for efficiency.

Representation:
---------------
A pipe dream is an int.

The bit for cell (r, c) is 1 exactly when that cell is crossed.
The bit index is the row-major index in the staircase:

    row 0: (0,0), (0,1), ..., (0,n-2)
    row 1: (1,0), (1,1), ..., (1,n-3)
    ...

So for S_n, there are n(n-1)/2 valid bits.

Example:
    D = pipe_dream_from_cells({(0, 0), (0, 1), (0, 3)}, n)

Rows and columns are 0-indexed.

For permutations in S_n, the staircase grid is:

    r >= 0,
    c >= 0,
    r + c <= n - 2.

A cross at cell (r, c) contributes the simple transposition

    s_{r+c+1}.
"""

from __future__ import annotations

from collections import defaultdict, deque
from itertools import combinations
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple


Cell = Tuple[int, int]
PipeDream = int
Permutation = Tuple[int, ...]
PipePair = Tuple[int, int]


# ---------------------------------------------------------------------
# Permutation utilities
# ---------------------------------------------------------------------

def validate_permutation(w: Sequence[int]) -> None:
    """
    Check that w is a permutation of 1, 2, ..., n.
    """
    n = len(w)

    if n == 0:
        raise ValueError("The permutation cannot be empty.")

    if sorted(w) != list(range(1, n + 1)):
        raise ValueError(f"{list(w)} is not a valid permutation of 1, 2, ..., {n}.")


def inversion_length(p: Sequence[int]) -> int:
    """
    Return the number of inversions of a permutation.
    """
    return sum(
        1
        for i in range(len(p))
        for j in range(i + 1, len(p))
        if p[i] > p[j]
    )


def apply_simple_transposition(p: Sequence[int], k: int) -> Permutation:
    """
    Apply s_k to p.

    In one-line notation, this swaps positions k and k+1.
    """
    n = len(p)

    if not (1 <= k < n):
        raise ValueError(f"s_{k} is not valid for a permutation in S_{n}.")

    q = list(p)
    q[k - 1], q[k] = q[k], q[k - 1]

    return tuple(q)


# ---------------------------------------------------------------------
# Cell / grid / bitmap utilities
# ---------------------------------------------------------------------

def cell_count(n: int) -> int:
    """
    Return the number of cells in the S_n staircase.
    """
    if n <= 0:
        raise ValueError("n must be positive.")

    return n * (n - 1) // 2


def valid_cell(cell: Cell, n: int) -> bool:
    """
    Return True if cell lies in the S_n staircase.
    """
    r, c = cell
    return 0 <= r < n - 1 and 0 <= c < n - 1 - r


def staircase_cells(n: int) -> List[Cell]:
    """
    Return all cells in the S_n staircase in row-major order.
    This is also the bit order.
    """
    if n <= 0:
        raise ValueError("n must be positive.")

    cells: List[Cell] = []

    for r in range(n - 1):
        for c in range(n - 1 - r):
            cells.append((r, c))

    return cells


def cell_index(cell: Cell, n: int) -> int:
    """
    Return the bit index for a valid staircase cell.

    The index is row-major in the staircase, not in an n by n square.
    """
    if not valid_cell(cell, n):
        raise ValueError(f"Cell {cell} is not valid for S_{n}.")

    r, c = cell
    cells_before_row = r * (n - 1) - r * (r - 1) // 2
    return cells_before_row + c


def cell_bit(cell: Cell, n: int) -> int:
    """
    Return the bit mask corresponding to a valid staircase cell.
    """
    return 1 << cell_index(cell, n)


def has_cross(D: PipeDream, cell: Cell, n: int) -> bool:
    """
    Return True exactly when cell is crossed in D.
    """
    return bool(D & cell_bit(cell, n))


def add_cross(D: PipeDream, cell: Cell, n: int) -> PipeDream:
    """
    Return D with cell set to a cross.
    """
    return D | cell_bit(cell, n)


def remove_cross(D: PipeDream, cell: Cell, n: int) -> PipeDream:
    """
    Return D with cell set to an elbow.
    """
    return D & ~cell_bit(cell, n)


def toggle_cell(D: PipeDream, cell: Cell, n: int) -> PipeDream:
    """
    Flip one cell between cross and elbow.
    """
    return D ^ cell_bit(cell, n)


def toggle_two_cells(D: PipeDream, cell1: Cell, cell2: Cell, n: int) -> PipeDream:
    """
    Flip two cells between cross and elbow.
    """
    return D ^ cell_bit(cell1, n) ^ cell_bit(cell2, n)


def pipe_dream_from_cells(cells: Iterable[Cell], n: int) -> PipeDream:
    """
    Convert an iterable of crossed cells into the bitmap representation.
    """
    D = 0

    for cell in cells:
        D = add_cross(D, cell, n)

    return D


def cells_from_pipe_dream(D: PipeDream, n: int) -> List[Cell]:
    """
    Convert a bitmap pipe dream into a sorted list of crossed cells.
    """
    check_pipe_dream_cells(D, n)

    return [cell for cell in staircase_cells(n) if has_cross(D, cell, n)]


def check_pipe_dream_cells(D: PipeDream, n: int) -> None:
    """
    Raise an error if D has bits outside the S_n staircase.
    """
    if D < 0:
        raise ValueError("A bitmap pipe dream must be a nonnegative integer.")

    allowed_bits = cell_count(n)

    if D >> allowed_bits:
        raise ValueError(
            f"Pipe dream has bits outside the S_{n} staircase. "
            f"S_{n} has only {allowed_bits} staircase cells."
        )


def cross_count(D: PipeDream) -> int:
    """
    Return the number of crossed cells.
    """
    return D.bit_count()


def cell_generator(cell: Cell) -> int:
    """
    A cross at cell (r, c) contributes s_{r+c+1}.
    """
    r, c = cell
    return r + c + 1


def reading_cells(D: PipeDream, n: int) -> List[Cell]:
    """
    Return crossed cells in reading order.

    Rows are read top to bottom.
    Each row is read right to left.
    """
    check_pipe_dream_cells(D, n)

    result: List[Cell] = []

    for r in range(n - 1):
        row_start = r * (n - 1) - r * (r - 1) // 2
        for c in range(n - 2 - r, -1, -1):
            bit = 1 << (row_start + c)
            if D & bit:
                result.append((r, c))

    return result


def reading_word(D: PipeDream, n: int) -> List[int]:
    """
    Return the reading word of the pipe dream.

    Example output:
        [4, 2, 1]
    means:
        s_4 s_2 s_1.
    """
    return [cell_generator(cell) for cell in reading_cells(D, n)]


def pipe_pairs_at_cells(D: PipeDream, n: int) -> Dict[Cell, PipePair]:
    """
    For every tile in the staircase, find which two pipe labels meet there.

    The pair is stored in sorted order, so pipes (2, 5) and (5, 2)
    are treated as the same pair.

    We scan the staircase in reading order:
        rows top to bottom,
        each row right to left.

    At a crossed tile, the two pipes swap.
    At an elbow tile, the two pipes do not swap.
    """
    check_pipe_dream_cells(D, n)

    pipe_order = list(range(1, n + 1))
    pair_at_cell: Dict[Cell, PipePair] = {}

    for r in range(n - 1):
        row_start = r * (n - 1) - r * (r - 1) // 2

        for c in range(n - 2 - r, -1, -1):
            cell = (r, c)
            k = cell_generator(cell)

            pipe_a = pipe_order[k - 1]
            pipe_b = pipe_order[k]

            pair_at_cell[cell] = tuple(sorted((pipe_a, pipe_b)))

            bit = 1 << (row_start + c)
            if D & bit:
                pipe_order[k - 1], pipe_order[k] = pipe_order[k], pipe_order[k - 1]

    return pair_at_cell


# ---------------------------------------------------------------------
# Pipe permutation
# ---------------------------------------------------------------------

def pipe_permutation(D: PipeDream, n: int) -> Permutation:
    """
    Compute the ordinary permutation generated by D.

    This avoids constructing the reading word list. It just scans the bitmap
    directly in reading order and swaps whenever the bit is 1.
    """
    check_pipe_dream_cells(D, n)

    p = list(range(1, n + 1))

    for r in range(n - 1):
        row_start = r * (n - 1) - r * (r - 1) // 2

        for c in range(n - 2 - r, -1, -1):
            bit = 1 << (row_start + c)

            if D & bit:
                k = r + c + 1
                p[k - 1], p[k] = p[k], p[k - 1]

    return tuple(p)


def generates_permutation(D: PipeDream, w: Sequence[int]) -> bool:
    """
    Return True if D generates w.
    """
    validate_permutation(w)
    return pipe_permutation(D, len(w)) == tuple(w)


def is_reduced_pipe_dream(D: PipeDream, n: int) -> bool:
    """
    Return True if D is reduced.

    A pipe dream is reduced if the number of crosses equals the
    inversion length of its generated permutation.
    """
    perm = pipe_permutation(D, n)
    return cross_count(D) == inversion_length(perm)


def is_nonreduced_pipe_dream(D: PipeDream, n: int) -> bool:
    """
    Return True if D is not reduced.
    """
    return not is_reduced_pipe_dream(D, n)


# ---------------------------------------------------------------------
# Top pipe dream
# ---------------------------------------------------------------------

def top_pipe_dream(w: Sequence[int]) -> PipeDream:
    """
    Construct the usual reduced top pipe dream for w.

    For each value j, count how many larger values appear before j in w.
    Then place that many crosses at the top of column j.

    Internally columns are 0-indexed, so value j uses column j - 1.
    """
    validate_permutation(w)

    n = len(w)
    pos = {value: i for i, value in enumerate(w)}
    D: PipeDream = 0

    for value in range(1, n + 1):
        position = pos[value]
        count = sum(1 for i in range(position) if w[i] > value)

        c = value - 1

        for r in range(count):
            cell = (r, c)

            if valid_cell(cell, n):
                D = add_cross(D, cell, n)

    return D


# ---------------------------------------------------------------------
# Move helpers
# ---------------------------------------------------------------------

def _cells_by_pipe_pair_with_bits(D: PipeDream, n: int) -> Dict[PipePair, List[Tuple[Cell, int]]]:
    """
    Internal helper used by move generation.

    It groups cells by the pair of pipes that meet there, and it stores each
    cell's bit mask too, so neighbors can be generated by XOR without calling
    cell_index repeatedly.
    """
    check_pipe_dream_cells(D, n)

    pipe_order = list(range(1, n + 1))
    cells_by_pair: Dict[PipePair, List[Tuple[Cell, int]]] = defaultdict(list)

    for r in range(n - 1):
        row_start = r * (n - 1) - r * (r - 1) // 2

        for c in range(n - 2 - r, -1, -1):
            cell = (r, c)
            bit = 1 << (row_start + c)
            k = r + c + 1

            pipe_a = pipe_order[k - 1]
            pipe_b = pipe_order[k]
            pair = tuple(sorted((pipe_a, pipe_b)))

            cells_by_pair[pair].append((cell, bit))

            if D & bit:
                pipe_order[k - 1], pipe_order[k] = pipe_order[k], pipe_order[k - 1]

    return cells_by_pair


def same_pipe_pair_toggle_neighbors(
    D: PipeDream,
    n: int,
    *,
    include_chute: bool = True,
    include_double: bool = True,
    verify_permutation: bool = False,
) -> Iterator[PipeDream]:
    """
    Generate both generalized chute moves and double-cross flips.

    same pipe pair + different statuses = generalized chute move
    same pipe pair + same statuses      = double-cross flip

    In bitmap form, toggling two cells is just:

        E = D ^ bit1 ^ bit2
    """
    check_pipe_dream_cells(D, n)
    base_perm = pipe_permutation(D, n) if verify_permutation else None

    cells_by_pair = _cells_by_pipe_pair_with_bits(D, n)

    for cells in cells_by_pair.values():
        if len(cells) < 2:
            continue

        for (_, bit1), (_, bit2) in combinations(cells, 2):
            cell1_crossed = bool(D & bit1)
            cell2_crossed = bool(D & bit2)

            same_status = cell1_crossed == cell2_crossed
            different_status = not same_status

            if different_status and not include_chute:
                continue

            if same_status and not include_double:
                continue

            E = D ^ bit1 ^ bit2

            if verify_permutation and pipe_permutation(E, n) != base_perm:
                continue

            yield E


# ---------------------------------------------------------------------
# Move graph
# ---------------------------------------------------------------------

def neighbors(
    D: PipeDream,
    n: int,
    *,
    include_chute: bool = True,
    include_double: bool = True,
    verify_permutation: bool = False,
) -> Iterator[PipeDream]:
    yield from same_pipe_pair_toggle_neighbors(
        D,
        n,
        include_chute=include_chute,
        include_double=include_double,
        verify_permutation=verify_permutation,
    )


# ---------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------

def sorted_pipe_dreams(dreams: Iterable[PipeDream]) -> List[PipeDream]:
    """
    Sort pipe dreams first by number of crosses, then by raw bitmap value.
    """
    return sorted(dreams, key=lambda D: (cross_count(D), D))


def all_generalized_pipe_dreams_by_moves(
    w: Sequence[int],
    *,
    start: Optional[PipeDream] = None,
    max_states: Optional[int] = None,
    include_double_cross_flips: bool = True,
    verify_permutation: bool = True,
) -> List[PipeDream]:
    """
    Enumerate generalized pipe dreams for w by BFS from the top pipe dream.

    The allowed moves are:

        - generalized chute moves
        - inverse generalized chute moves
        - double-cross flips, if include_double_cross_flips=True

    The invariant is the pipe permutation.
    """
    validate_permutation(w)

    n = len(w)
    target = tuple(w)

    if start is None:
        start = top_pipe_dream(w)

    check_pipe_dream_cells(start, n)

    if pipe_permutation(start, n) != target:
        raise ValueError(
            "The starting pipe dream does not generate the target permutation "
            "under the ordinary product."
        )

    seen: Set[PipeDream] = {start}
    queue = deque([start])

    while queue:
        D = queue.popleft()

        for E in neighbors(
            D,
            n,
            include_chute=True,
            include_double=include_double_cross_flips,
            verify_permutation=False,
        ):
            if verify_permutation and pipe_permutation(E, n) != target:
                continue

            if E in seen:
                continue

            seen.add(E)
            queue.append(E)

            if max_states is not None and len(seen) >= max_states:
                return sorted_pipe_dreams(seen)

    return sorted_pipe_dreams(seen)


def all_pipe_dreams_by_filter(w: Sequence[int]) -> List[PipeDream]:
    """
    Brute-force all bitmap subsets of the staircase whose ordinary product is w.

    Warning:
    --------
    This grows very quickly.

        S_5:  2^10 = 1,024 states
        S_6:  2^15 = 32,768 states
        S_7:  2^21 = 2,097,152 states
    """
    validate_permutation(w)

    n = len(w)
    target = tuple(w)
    result: List[PipeDream] = []

    for D in range(1 << cell_count(n)):
        if pipe_permutation(D, n) == target:
            result.append(D)

    return sorted_pipe_dreams(result)


def reduced_pipe_dreams(w: Sequence[int]) -> List[PipeDream]:
    """
    Return reachable reduced pipe dreams for w.
    """
    n = len(w)
    dreams = all_generalized_pipe_dreams_by_moves(w)

    return [D for D in dreams if is_reduced_pipe_dream(D, n)]


def nonreduced_pipe_dreams(w: Sequence[int]) -> List[PipeDream]:
    """
    Return reachable non-reduced pipe dreams for w.
    """
    n = len(w)
    dreams = all_generalized_pipe_dreams_by_moves(w)

    return [D for D in dreams if not is_reduced_pipe_dream(D, n)]


def compare_moves_to_bruteforce(w: Sequence[int]) -> Tuple[bool, Set[PipeDream], Set[PipeDream]]:
    """
    Compare move-based enumeration with brute-force enumeration.

    Returns:
        (matches, missing, extra)

    missing = brute force states not reached by moves
    extra   = move-generated states not found by brute force
    """
    brute = set(all_pipe_dreams_by_filter(w))
    moves = set(all_generalized_pipe_dreams_by_moves(w))

    return brute == moves, brute - moves, moves - brute


# ---------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------

def to_matrix(D: PipeDream, n: int, *, square: bool = True) -> List[List[int]]:
    """
    Convert a pipe dream to a matrix of 0s and 1s.

    If square=True, return an n by n matrix.

    If square=False, return only the staircase rows.
    """
    check_pipe_dream_cells(D, n)

    if square:
        return [
            [1 if valid_cell((r, c), n) and has_cross(D, (r, c), n) else 0 for c in range(n)]
            for r in range(n)
        ]

    return [
        [1 if has_cross(D, (r, c), n) else 0 for c in range(n - 1 - r)]
        for r in range(n - 1)
    ]


def pipe_dream_to_string(
    D: PipeDream,
    n: int,
    *,
    cross_symbol: str = "+",
    empty_symbol: str = ".",
) -> str:
    """
    Return a printable staircase representation.
    """
    check_pipe_dream_cells(D, n)

    rows: List[str] = []

    for r in range(n - 1):
        pieces: List[str] = []

        for c in range(n - 1 - r):
            if has_cross(D, (r, c), n):
                pieces.append(cross_symbol)
            else:
                pieces.append(empty_symbol)

        rows.append(" ".join(pieces))

    return "\n".join(rows)


def print_pipe_dream(
    D: PipeDream,
    n: int,
    *,
    show_word: bool = True,
    show_perm: bool = True,
    show_cross_count: bool = True,
    show_reduced: bool = True,
    show_bitmap: bool = True,
) -> None:
    """
    Print a pipe dream and optional data.
    """
    print(pipe_dream_to_string(D, n))

    if show_bitmap:
        print("bitmap:", D)
        print("bits:", bin(D))

    if show_word:
        print("word:", reading_word(D, n))

    if show_perm:
        print("ordinary permutation:", pipe_permutation(D, n))

    if show_cross_count:
        print("crosses:", cross_count(D))

    if show_reduced:
        print("reduced:", is_reduced_pipe_dream(D, n))


def monomial_exponents(D: PipeDream, n: int) -> Tuple[int, ...]:
    """
    Return the exponent vector of the pipe dream monomial.

    Each cross in row r contributes one factor of x_{r+1}.
    """
    check_pipe_dream_cells(D, n)

    return tuple(
        sum(1 for c in range(n - 1 - r) if has_cross(D, (r, c), n))
        for r in range(n)
    )


# ---------------------------------------------------------------------
# Input parser and demo
# ---------------------------------------------------------------------

def parse_permutation(text: str) -> List[int]:
    """
    Parse a permutation from user input.

    Accepts:
        31254
        3 1 2 5 4
        3,1,2,5,4

    Note:
        Compact input like 31254 only works cleanly for n <= 9.
        For n >= 10, use spaces or commas.
    """
    text = text.strip()

    if not text:
        raise ValueError("Empty permutation input.")

    if "," in text:
        return [int(piece.strip()) for piece in text.split(",") if piece.strip()]

    if " " in text:
        return [int(piece.strip()) for piece in text.split() if piece.strip()]

    return [int(ch) for ch in text]
