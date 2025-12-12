# environment.py
from typing import List, Optional

class TicTacToeEnvironment:
    """
    負責：
    - 儲存棋盤狀態
    - 檢查合法步
    - 判斷勝負 / 平手
    - 管理輪到誰下
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """重設棋盤"""
        # None 代表空格, 'X' / 'O' 代表玩家
        self.board: List[Optional[str]] = [None] * 9
        self.current_player: str = 'X'
        self.winner: Optional[str] = None
        self.done: bool = False

    def available_actions(self) -> List[int]:
        """回傳所有可以下的位置 index (0~8)"""
        return [i for i, cell in enumerate(self.board) if cell is None]

    def step(self, action: int) -> None:
        """
        讓 current_player 在 action 位置下棋。
        如果 action 不合法，丟出例外。
        """
        if self.done:
            raise ValueError("Game already finished.")
        if action not in self.available_actions():
            raise ValueError(f"Invalid action: {action}")

        self.board[action] = self.current_player
        self.winner = self._check_winner()

        if self.winner is not None:
            self.done = True
        elif not self.available_actions():
            # 沒有空格且沒人贏 => 平手
            self.done = True
        else:
            # 換人
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def _check_winner(self) -> Optional[str]:
        """檢查是否有勝利者，有的話回傳 'X' 或 'O'，否則 None。"""
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 橫列
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 直行
            (0, 4, 8), (2, 4, 6)              # 斜線
        ]

        for a, b, c in lines:
            if self.board[a] is not None and \
               self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def render_text(self) -> str:
        """回傳文字版棋盤（可以在 terminal demo 時使用）"""
        def cell(i):
            return self.board[i] if self.board[i] is not None else ' '
        rows = []
        for r in range(3):
            rows.append(f" {cell(3*r)} | {cell(3*r+1)} | {cell(3*r+2)} ")
        return "\n---+---+---\n".join(rows)
