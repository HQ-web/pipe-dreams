from enum import IntEnum

# ordinary
class OTile(IntEnum):
    ELBOW = 0
    CROSS = 1

# chained generic
class GTile(IntEnum):
    BLANK = 0
    HORIZONTAL = 1
    VERTICAL = 2
    TURN_NW = 3
    TURN_SE = 4
    CROSS = 5
    BUMP_DIFF = 6
    BUMP_SAME = 7

# rectangles[k][row][col] is a GTile code
cgpd = [
    [
        [GTile.CROSS, GTile.TURN_SE],
        [GTile.VERTICAL, GTile.BLANK],
    ],
    [
        [GTile.BUMP_DIFF],
        [GTile.HORIZONTAL],
    ],
]