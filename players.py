from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List
import random


# ========= 基底 Player 類別 =========

class Player(ABC):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol  # 'X' 或 'O'

    @abstractmethod
    def select_action(self, env) -> Optional[int]:
        """
        回傳要下的格子 index（0~8），若無可下位置可回傳 None。
        """
        raise NotImplementedError


# ========= Human 玩家 =========

class HumanPlayer(Player):
    """
    由 GUI 幫他設定下一步要下哪格（set_next_action），
    select_action 只是把這個值吐回去。
    """

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)
        self._next_action: Optional[int] = None

    def set_next_action(self, action: int) -> None:
        self._next_action = action

    def select_action(self, env) -> Optional[int]:
        # 這裡假設 GUI 已經確保 action 合法
        return self._next_action


# ========= AI Strategy 介面（策略模式核心） =========

class AIStrategy(ABC):
    """
    所有 AI 策略的共同介面：
    在當前 env 下，決定要選哪一個 action（0~8）。
    """

    @abstractmethod
    def choose_action(self, env) -> Optional[int]:
        raise NotImplementedError


# ========= 具體策略：Easy - 亂數 AI =========

class RandomStrategy(AIStrategy):
    def choose_action(self, env) -> Optional[int]:
        actions: List[int] = env.available_actions()
        if not actions:
            return None
        return random.choice(actions)


# ========= 具體策略：Medium - 簡單規則 AI =========
"""
Medium 策略邏輯：
1. 如果有一步可以讓自己立刻獲勝 → 下那格
2. 否則，如果對手下一步會獲勝 → 優先擋對手
3. 否則，如果中間(4)有空 → 下中間
4. 否則，隨機從剩下合法位置中選一格
"""

class MediumStrategy(AIStrategy):
    def __init__(self, ai_symbol: str) -> None:
        self.ai_symbol = ai_symbol
        self.op_symbol = 'O' if ai_symbol == 'X' else 'X'

    def choose_action(self, env) -> Optional[int]:
        actions: List[int] = env.available_actions()
        if not actions:
            return None

        board: List[Optional[str]] = env.board

        # 1. 嘗試找到「自己可以直接獲勝」的一步
        for a in actions:
            new_board = board.copy()
            new_board[a] = self.ai_symbol
            if self._check_winner(new_board) == self.ai_symbol:
                return a

        # 2. 嘗試擋對手：如果對手下一步會贏，就先佔那格
        for a in actions:
            new_board = board.copy()
            new_board[a] = self.op_symbol
            if self._check_winner(new_board) == self.op_symbol:
                return a

        # 3. 佔中間（位置 index=4），如果有空
        if 4 in actions:
            return 4

        # 4. 其他情況 → 隨機
        return random.choice(actions)

    def _check_winner(self, board: List[Optional[str]]) -> Optional[str]:
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if board[a] is not None and board[a] == board[b] == board[c]:
                return board[a]
        return None


# ========= 具體策略：Hard - Minimax AI =========

class MinimaxStrategy(AIStrategy):
    """
    標準的 Minimax，用當前棋盤直接評估。
    不去改動真正的 env，只操作 board 的 copy。
    """

    def __init__(self, ai_symbol: str) -> None:
        self.ai_symbol = ai_symbol
        self.op_symbol = 'O' if ai_symbol == 'X' else 'X'

    def choose_action(self, env) -> Optional[int]:
        actions: List[int] = env.available_actions()
        if not actions:
            return None

        best_score = float('-inf')
        best_action: Optional[int] = None

        board = env.board  # 預設是長度 9 的 list[Optional[str]]

        for action in actions:
            new_board = board.copy()
            new_board[action] = self.ai_symbol
            score = self._minimax(new_board, self.op_symbol)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    # ----- Minimax 遞迴 -----

    def _minimax(self, board: List[Optional[str]], current_symbol: str) -> float:
        winner = self._check_winner(board)
        if winner == self.ai_symbol:
            return 1.0
        elif winner == self.op_symbol:
            return -1.0
        elif all(c is not None for c in board):
            return 0.0  # 平手

        # 輪到誰下
        is_ai_turn = (current_symbol == self.ai_symbol)

        if is_ai_turn:
            best_score = float('-inf')
            for idx in range(9):
                if board[idx] is None:
                    board[idx] = self.ai_symbol
                    score = self._minimax(board, self.op_symbol)
                    board[idx] = None
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for idx in range(9):
                if board[idx] is None:
                    board[idx] = self.op_symbol
                    score = self._minimax(board, self.ai_symbol)
                    board[idx] = None
                    best_score = min(best_score, score)
            return best_score

    def _check_winner(self, board: List[Optional[str]]) -> Optional[str]:
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if board[a] is not None and board[a] == board[b] == board[c]:
                return board[a]
        return None


# ========= AI Player：持有「策略」的玩家 =========

class AIPlayer(Player):
    """
    通用 AI 玩家，不管你是 Random / Medium / Minimax / 其他 AI，
    都是透過 AIStrategy 來決定要下哪一格。
    """

    def __init__(self, symbol: str, strategy: AIStrategy) -> None:
        super().__init__(symbol)
        self.strategy = strategy

    def select_action(self, env) -> Optional[int]:
        return self.strategy.choose_action(env)


# ========= 對外相容用的名稱（保留原本 API） =========

class RandomAIPlayer(AIPlayer):
    """
    原本的 RandomAIPlayer，現在變成：
    - 一個 AIPlayer
    - 搭配 RandomStrategy 當作「頭腦」
    """

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol, RandomStrategy())


class MediumAIPlayer(AIPlayer):
    """
    新增的 MediumAIPlayer：
    - 使用 MediumStrategy（簡單規則 + 部分防守）
    """

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol, MediumStrategy(symbol))


class MinimaxAIPlayer(AIPlayer):
    """
    原本的 MinimaxAIPlayer，現在變成：
    - 一個 AIPlayer
    - 搭配 MinimaxStrategy 當作「頭腦」
    """

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol, MinimaxStrategy(symbol))