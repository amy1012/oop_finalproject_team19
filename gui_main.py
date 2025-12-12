# gui_main.py
import tkinter as tk
from typing import Optional
from game_manager import GameManager, GameMode


class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("OOP Tic-Tac-Toe")
        self.manager: Optional[GameManager] = None
        self.buttons = []
        self.status_label: Optional[tk.Label] = None

        self._build_mode_selection()

    # ---------- 首頁：選擇模式 ----------

    def _build_mode_selection(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        label = tk.Label(frame, text="請選擇模式", font=("Arial", 16))
        label.pack(pady=10)

        btn_ai_human = tk.Button(
            frame, text="AI 對 人類", width=15,
            command=lambda: self._start_game("ai_vs_human")
        )
        btn_ai_human.pack(pady=5)

        btn_ai_ai = tk.Button(
            frame, text="AI 對 AI", width=15,
            command=lambda: self._start_game("ai_vs_ai")
        )
        btn_ai_ai.pack(pady=5)

        self.mode_frame = frame

    # ---------- 建立遊戲畫面 ----------

    def _start_game(self, mode: GameMode) -> None:
        self.mode_frame.destroy()
        self.manager = GameManager(mode)
        self.manager.reset()

        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20)

        # 狀態列
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # 3x3 棋盤按鈕
        for i in range(9):
            btn = tk.Button(
                main_frame, text=" ", font=("Arial", 24),
                width=3, height=1,
                command=lambda idx=i: self._on_cell_clicked(idx)
            )
            btn.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # reset 按鈕
        reset_btn = tk.Button(
            main_frame, text="重新開始", command=self._reset_game
        )
        reset_btn.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        self._update_ui()

        # 如果是 AI 對 AI，啟動自動對戰
        if mode == "ai_vs_ai":
            self._ai_vs_ai_loop()

    # ---------- 遊戲流程 ----------

    def _reset_game(self) -> None:
        if self.manager is None:
            return
        self.manager.reset()
        self._update_ui()
        if self.manager.mode == "ai_vs_ai":
            self._ai_vs_ai_loop()

    def _on_cell_clicked(self, idx: int) -> None:
        if self.manager is None or self.manager.env.done:
            return
        if self.manager.mode != "ai_vs_human":
            return  # 在 AI vs AI 模式下，按按鈕沒用

        # 人類下棋
        self.manager.human_move(idx)
        self._update_ui()

        # 若遊戲還沒結束，輪到 AI
        if not self.manager.env.done:
            self.root.after(400, self._ai_move_once)

    def _ai_move_once(self) -> None:
        if self.manager is None or self.manager.env.done:
            return
        self.manager.ai_move()
        self._update_ui()

    def _ai_vs_ai_loop(self) -> None:
        """AI 對 AI 的自動迴圈"""
        if self.manager is None or self.manager.env.done:
            return
        # 每 500ms 讓一個 AI 下棋
        self.manager.ai_move()
        self._update_ui()
        if not self.manager.env.done:
            self.root.after(500, self._ai_vs_ai_loop)

    # ---------- UI 更新 ----------

    def _update_ui(self) -> None:
        if self.manager is None:
            return
        env = self.manager.env

        # 更新棋盤按鈕文字與可用性
        for i, btn in enumerate(self.buttons):
            value = env.board[i]
            btn.config(text=value if value is not None else " ")
            if env.done or value is not None:
                btn.config(state="disabled")
            else:
                btn.config(state="normal")

        # 更新狀態列
        if self.status_label is None:
            return

        if env.done:
            if env.winner is None:
                self.status_label.config(text="平手！")
            else:
                self.status_label.config(text=f"{env.winner} 勝利！")
        else:
            self.status_label.config(text=f"輪到 {env.current_player}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
