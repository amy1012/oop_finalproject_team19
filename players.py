# players.py
from abc import ABC, abstractmethod
from typing import Optional
from environment import TicTacToeEnvironment
import random


class Player(ABC):
    """
    抽象玩家：
    - 擁有 symbol ('X' 或 'O')
    - 透過 select_action(env) 決定下一步
    """

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    @abstractmethod
    def select_action(self, env: TicTacToeEnvironment) -> int:
        """回傳要下的位置 (0~8)"""
        pass


class RandomAIPlayer(Player):
    """簡單 AI：隨機在可下的位置中選一個"""

    def select_action(self, env: TicTacToeEnvironment) -> int:
        actions = env.available_actions()
        return random.choice(actions)


class HumanPlayer(Player):
    """
    HumanPlayer 不直接讀 input，
    由 GUI 把玩家按的格子傳進來。
    """

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)
        self._next_action: Optional[int] = None

    def set_next_action(self, action: int) -> None:
        self._next_action = action

    def select_action(self, env: TicTacToeEnvironment) -> int:
        if self._next_action is None:
            raise RuntimeError("Human move not set yet.")
        action = self._next_action
        self._next_action = None
        return action


class MinimaxAIPlayer(Player):
    """
    比較聰明的 AI，用 minimax 找「最佳步」。
    """

    def select_action(self, env: TicTacToeEnvironment) -> int:
        best_score = None
        best_action = None
        for action in env.available_actions():
            # 模擬一步
            env_copy = self._copy_env(env)
            env_copy.step(action)
            score = self._minimax(env_copy, False)
            if best_score is None or score > best_score:
                best_score = score
                best_action = action
        assert best_action is not None
        return best_action

    def _minimax(self, env: TicTacToeEnvironment, is_max_turn: bool) -> int:
        # 終局評分
        if env.done:
            if env.winner == self.symbol:
                return 1
            elif env.winner is None:
                return 0
            else:
                return -1

        if is_max_turn:
            best_score = -999
            for action in env.available_actions():
                env_copy = self._copy_env(env)
                env_copy.step(action)
                score = self._minimax(env_copy, False)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = 999
            for action in env.available_actions():
                env_copy = self._copy_env(env)
                env_copy.step(action)
                score = self._minimax(env_copy, True)
                best_score = min(best_score, score)
            return best_score

    def _copy_env(self, env: TicTacToeEnvironment) -> TicTacToeEnvironment:
        new_env = TicTacToeEnvironment()
        new_env.board = env.board.copy()
        new_env.current_player = env.current_player
        new_env.winner = env.winner
        new_env.done = env.done
        return new_env
