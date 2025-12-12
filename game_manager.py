# game_manager.py
from typing import Literal, Optional
from environment import TicTacToeEnvironment
from players import (
    Player,
    HumanPlayer,
    RandomAIPlayer,
    MediumAIPlayer,
    MinimaxAIPlayer,
)
import random  # 用來隨機決定先手


GameMode = Literal["ai_vs_ai", "ai_vs_human"]
Difficulty = Literal["easy", "medium", "hard"]


class GameManager:
    """
    負責：
    - 建立 environment + players
    - 控管輪流下棋
    - 提供 GUI 呼叫的方法
    """

    def __init__(self, mode: GameMode, difficulty: Difficulty = "hard") -> None:
        self.mode: GameMode = mode
        self.difficulty: Difficulty = difficulty
        self.env = TicTacToeEnvironment()

        if mode == "ai_vs_ai":
            # ✅ 做法 A：難度同時套用到 X / O 兩個 AI
            if difficulty == "easy":
                self.player_X: Player = RandomAIPlayer('X')
                self.player_O: Player = RandomAIPlayer('O')
            elif difficulty == "medium":
                self.player_X = MediumAIPlayer('X')
                self.player_O = MediumAIPlayer('O')
            else:  # "hard"
                self.player_X = MinimaxAIPlayer('X')
                self.player_O = MinimaxAIPlayer('O')

        elif mode == "ai_vs_human":
            # 人類當 X，AI 當 O，AI 策略依照難度決定
            self.player_X = HumanPlayer('X')

            if difficulty == "easy":
                self.player_O = RandomAIPlayer('O')
            elif difficulty == "medium":
                self.player_O = MediumAIPlayer('O')
            else:  # "hard"
                self.player_O = MinimaxAIPlayer('O')
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        # 隨機決定這一局由 X 還是 O 先手
        self.env.current_player = random.choice(['X', 'O'])

    def reset(self) -> None:
        self.env.reset()
        # 重新開始遊戲時，也重新隨機先手
        self.env.current_player = random.choice(['X', 'O'])

    def get_current_player(self) -> Player:
        return self.player_X if self.env.current_player == 'X' else self.player_O

    # 給 GUI 用：現在是不是人類回合？
    def is_current_player_human(self) -> bool:
        return isinstance(self.get_current_player(), HumanPlayer)

    def human_move(self, action: int) -> None:
        """
        給 GUI 用：當使用者在某個格子按下去時呼叫。
        只允許在 human 回合呼叫。
        """
        player = self.get_current_player()
        if not isinstance(player, HumanPlayer):
            # 如果現在不是人類回合，就忽略
            return
        if action not in self.env.available_actions():
            return
        player.set_next_action(action)
        chosen = player.select_action(self.env)
        self.env.step(chosen)

    def ai_move(self) -> Optional[int]:
        """
        給 GUI 用：輪到 AI 回合時，執行一次 AI 下棋。
        回傳 AI 下的格子 index，若無法下（結束）則回傳 None。
        """
        if self.env.done:
            return None
        player = self.get_current_player()
        if isinstance(player, HumanPlayer):
            # 現在是人類回合，不該呼叫 ai_move
            return None
        action = player.select_action(self.env)
        self.env.step(action)
        return action