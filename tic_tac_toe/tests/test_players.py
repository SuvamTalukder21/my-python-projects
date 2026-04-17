import pytest
import random

from src.players.base import BasePlayer
from src.players.human import HumanPlayer
from src.players.cpu import CPUPlayer
from src.game.board import Board
from src.utils.constants import PLAYER_X, PLAYER_O, EMPTY


class DummyPlayer(BasePlayer):
    def make_move(self, board):
        return (0, 0)


@pytest.fixture
def board():
    return Board()


# ---------------------------
# Base Player Tests
# ---------------------------

def test_base_player_score_increment_and_reset():
    p = DummyPlayer(PLAYER_X, 'Dummy')

    assert p.score == 0
    p.increment_score()
    assert p.score == 1

    p.reset_score()
    assert p.score == 0


# ---------------------------
# Human Player Tests
# ---------------------------

def test_human_player_make_move_valid(monkeypatch, board):
    human = HumanPlayer(PLAYER_X, 'Tester')

    # simulate user entering "1 1"
    monkeypatch.setattr('builtins.input', lambda _: '1 1')

    move = human.make_move(board)
    assert move == (0, 0)


def test_human_player_invalid_then_valid(monkeypatch, board):
    human = HumanPlayer(PLAYER_X, 'Tester')

    # first invalid, then valid
    inputs = iter(['invalid', '1 1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    move = human.make_move(board)
    assert move == (0, 0)


# ---------------------------
# CPU Player (Easy / Medium)
# ---------------------------

def test_cpu_random_move(monkeypatch, board):
    cpu = CPUPlayer(PLAYER_O, difficulty='Easy')

    board.make_move(0, 0, PLAYER_X)
    board.make_move(1, 1, PLAYER_X)

    monkeypatch.setattr(random, 'choice', lambda lst: lst[0])

    move = cpu.random_move(board)
    assert move == board.get_available_moves()[0]


def test_cpu_medium_move(board):
    cpu = CPUPlayer(PLAYER_X, difficulty='Medium')

    board.make_move(0, 0, PLAYER_O)
    board.make_move(1, 1, PLAYER_O)

    available = board.get_available_moves()
    expected = available[len(available) // 2]

    assert cpu.medium_move(board) == expected


# ---------------------------
# CPU Player (Hard / Minimax)
# ---------------------------

def test_cpu_hard_blocks_opponent(board):
    cpu = CPUPlayer(PLAYER_O, difficulty='Hard')

    # X about to win
    board.make_move(0, 0, PLAYER_X)
    board.make_move(0, 1, PLAYER_X)

    move = cpu.best_move(board)

    assert move == (0, 2)  # must block


def test_cpu_hard_wins_when_possible(board):
    cpu = CPUPlayer(PLAYER_O, difficulty='Hard')

    # O can win
    board.make_move(1, 0, PLAYER_O)
    board.make_move(1, 1, PLAYER_O)

    move = cpu.best_move(board)

    assert move == (1, 2)


def test_cpu_hard_returns_none_on_full_board(board):
    cpu = CPUPlayer(PLAYER_X, difficulty='Hard')

    # Fill board
    for r in range(3):
        for c in range(3):
            board.make_move(r, c, PLAYER_X)

    move = cpu.best_move(board)
    assert move is None


def test_cpu_hard_prefers_center_first(board):
    cpu = CPUPlayer(PLAYER_X, difficulty='Hard')

    # Empty board → best move is usually center
    move = cpu.best_move(board)

    assert move in [(0,0), (0,2), (2,0), (2,2), (1,1)]
