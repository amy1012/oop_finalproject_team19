# game_manager.py
from typing import Literal, Optional
from environment import TicTacToeEnvironment
from players import Player, HumanPlayer, RandomAIPlayer, MinimaxAIPlayer
import random  # ✅ 新增：用來隨機決定先手


GameMode = Literal["ai_vs_ai", "ai_vs_human"]


class GameManager:
    """
    負責：
    - 建立 environment + players
    - 控管輪流下棋
    - 提供 GUI 呼叫的方法
    """

    def __init__(self, mode: GameMode) -> None:
        self.mode: GameMode = mode
        self.env = TicTacToeEnvironment()

        if mode == "ai_vs_ai":
            # 你可以自己調整組合：Minimax vs Random、Minimax vs Minimax 都可
            self.player_X: Player = MinimaxAIPlayer('X')
            self.player_O: Player = RandomAIPlayer('O')
        elif mode == "ai_vs_human":
            # 人類當 X，AI 當 O
            self.player_X = HumanPlayer('X')
            self.player_O = MinimaxAIPlayer('O')
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
        self.env.current_player = random.choice(['X', 'O'])  # 隨機決定先手

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