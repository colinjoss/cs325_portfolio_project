# Name: Colin Joss
# Date: 8-2-2021
# Class: CS 325
# Assignment: Homework #5

from collections import deque

Board = [
    ['-', '-', '-', '-', '-'],
    ['-', '-', '#', '-', '-'],
    ['-', '-', '-', '-', '-'],
    ['#', '-', '#', '#', '-'],
    ['-', '#', '-', '-', '-']
]

Source = (1, 1)
Destination = (5, 5)


def solve_puzzle(Board, Source, Destination):
    """
    Finds the shortest from the Source to the Destination using BFS and a string
    of directions representing a possible path.
    """
    if Board[Destination[0]-1][Destination[1]-1] == '#':  # If destination is blocked space, return None
        return None

    Memo = [[float('inf')] * len(Board[0])]  # Create memo
    for row in range(1, len(Board)):
        Memo.append([float('inf')] * len(Board[0]))
    Memo[Source[0]-1][Source[1]-1] = 0

    dist = solve_puzzle_helper(Board, Source, Destination, Memo)  # Find distance
    if dist is None:  # If impossible to reach, return None
        return None

    seq = solve_puzzle_optimal(Board, Destination, Memo)  # Find an optimal sequence (EXTRA CREDIT)
    return dist, seq


def solve_puzzle_helper(brd, src, dest, memo):
    """
    Returns the shortest number of steps from the source to the destination.
    """
    queue = deque()
    queue.append(src)

    while queue:
        cur = queue.popleft()
        if memo[dest[0]-1][dest[1]-1] != float('inf'):  # If destination logged in memo
            return memo[dest[0] - 1][dest[1] - 1] - 1

        neighbors = get_unvisited_neighbors(cur, brd, memo)  # Get neighboring nodes
        for node in neighbors:
            if brd[node[0] - 1][node[1] - 1] == '#':  # If blocked, assign None in memo
                memo[node[0] - 1][node[1] - 1] = None
            else:  # If free, increment dist by 1 in memo & add to queue
                memo[node[0] - 1][node[1] - 1] = memo[cur[0] - 1][cur[1] - 1] + 1
                queue.append(node)
    return None


def get_unvisited_neighbors(node, brd, memo):
    """
    Returns a list of valid neighboring nodes.
    """
    neighbors = []
    for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        nc = (node[0] + dir[0], node[1] + dir[1])
        if 0 < nc[0] <= len(brd) and 0 < nc[1] <= len(brd[0]) and memo[nc[0]-1][nc[1]-1] == float('inf'):
            neighbors.append(nc)  # Neighbor is valid if on the board and unqueued
    return neighbors


def solve_puzzle_optimal(brd, dest, memo, result=''):
    """
    Backtracks through a completed memo to reassemble a possible optimal
    sequence of instructions.
    *EXTRA CREDIT*
    """
    x, y = dest[0], dest[1]
    for i in range(memo[dest[0]-1][dest[1]-1], 0, -1):
        for dir in [(-1, 0, 'D'), (0, 1, 'L'), (1, 0, 'U'), (0, -1, 'R')]:
            a, b = x + dir[0], y + dir[1]
            if 0 < a <= len(brd) and 0 < b <= len(brd[0]) and memo[a-1][b-1] == i-1:
                x, y = a, b
                result = dir[2] + result
                break
    return result
