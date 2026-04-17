import pytest

from src.game.board import Board
from src.game.engine import GameEngine
from src.utils.constants import (
    GAME_ONGOING,
    GAME_WIN,
    GAME_DRAW,
    PLAYER_X,
    PLAYER_O
)


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def engine(board):
    return GameEngine(board)


@pytest.mark.parametrize("moves, player", [
    # Row win
    ([(0, 0), (0, 1), (0, 2)], PLAYER_X),

    # Column win
    ([(0, 1), (1, 1), (2, 1)], PLAYER_O),

    # Main diagonal
    ([(0, 0), (1, 1), (2, 2)], PLAYER_X),

    # Anti-diagonal
    ([(0, 2), (1, 1), (2, 0)], PLAYER_O),
])
def test_check_winner_all_cases(board, engine, moves, player):
    board.reset()

    for r, c in moves:
        board.make_move(r, c, player)

    assert engine.check_winner(player) is True


def test_check_winner_negative_case(board, engine):
    """Ensure no false positives for winner"""
    board.make_move(0, 0, PLAYER_X)
    board.make_move(0, 1, PLAYER_X)

    assert engine.check_winner(PLAYER_X) is False


def test_get_game_status_ongoing(board, engine):
    assert engine.get_game_status(PLAYER_X) == GAME_ONGOING


def test_get_game_status_win(board, engine):
    board.make_move(0, 0, PLAYER_X)
    board.make_move(0, 1, PLAYER_X)
    board.make_move(0, 2, PLAYER_X)

    assert engine.get_game_status(PLAYER_X) == GAME_WIN


def test_get_game_status_draw(board, engine):
    moves = [
        (0, 0, PLAYER_X), (0, 1, PLAYER_O), (0, 2, PLAYER_X),
        (1, 0, PLAYER_X), (1, 1, PLAYER_O), (1, 2, PLAYER_O),
        (2, 0, PLAYER_O), (2, 1, PLAYER_X), (2, 2, PLAYER_X),
    ]

    for r, c, p in moves:
        board.make_move(r, c, p)

    assert board.is_full() is True
    assert engine.get_game_status(PLAYER_O) == GAME_DRAW


def test_draw_no_false_winner(board, engine):
    """Ensure draw board does not falsely detect winner"""
    moves = [
        (0, 0, PLAYER_X), (0, 1, PLAYER_O), (0, 2, PLAYER_X),
        (1, 0, PLAYER_X), (1, 1, PLAYER_O), (1, 2, PLAYER_O),
        (2, 0, PLAYER_O), (2, 1, PLAYER_X), (2, 2, PLAYER_X),
    ]

    for r, c, p in moves:
        board.make_move(r, c, p)

    assert engine.check_winner(PLAYER_X) is False
    assert engine.check_winner(PLAYER_O) is False
