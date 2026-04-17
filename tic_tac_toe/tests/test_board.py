import pytest

from src.game.board import Board
from src.utils.constants import EMPTY, PLAYER_X, PLAYER_O


@pytest.fixture
def board():
    """Reusable Board instance"""
    return Board()


def test_create_empty_board(board):
    assert board.size == 3
    assert all(cell == EMPTY for row in board.grid for cell in row)


def test_make_move_and_is_valid_move(board):
    # valid move
    assert board.is_valid_move(0, 0) is True

    # place X
    assert board.make_move(0, 0, PLAYER_X) is True
    assert board.grid[0][0] == PLAYER_X

    # same cell should now be invalid
    assert board.is_valid_move(0, 0) is False
    assert board.make_move(0, 0, PLAYER_O) is False


def test_out_of_bounds_move(board):
    assert board.is_valid_move(-1, 0) is False
    assert board.is_valid_move(3, 3) is False


def test_is_full_and_get_available_moves(board):
    moves = [(r, c) for r in range(board.size) for c in range(board.size)]

    # fill all but last position
    for r, c in moves[:-1]:
        board.make_move(r, c, PLAYER_X)

    assert board.is_full() is False

    available = board.get_available_moves()
    assert available == [moves[-1]]

    # fill last cell
    last_r, last_c = moves[-1]
    board.make_move(last_r, last_c, PLAYER_O)

    assert board.is_full() is True
    assert board.get_available_moves() == []


def test_reset(board):
    board.make_move(0, 0, PLAYER_X)
    board.reset()

    assert all(cell == EMPTY for row in board.grid for cell in row)
    assert len(board.grid) == 3


# def test_undo_move(board):
#     board.make_move(1, 1, PLAYER_X)
#     board.make_move(1, 1, EMPTY)  # undo
#
#     assert board.grid[1][1] == EMPTY


@pytest.mark.parametrize("row,col", [
    (0, 0),
    (1, 1),
    (2, 2),
])
def test_valid_moves_multiple_positions(board, row, col):
    assert board.is_valid_move(row, col) is True
    board.make_move(row, col, PLAYER_X)
    assert board.grid[row][col] == PLAYER_X
