# gui_main.py
import tkinter as tk
from typing import Optional
from game_manager import GameManager, GameMode, Difficulty


class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("OOP Tic-Tac-Toe")
        # self.root.geometry("420x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f8")

        self.manager: Optional[GameManager] = None
        self.buttons = []
        self.status_label: Optional[tk.Label] = None

        # 難度選擇（預設 Hard）
        self.difficulty_var = tk.StringVar(value="hard")

        # ===== 多局戰績統計 =====
        self.total_games = 0
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.game_recorded = False  # 這一局的結果是否已經計入戰績

        # 主畫面上的戰績 Label
        self.stats_total_label: Optional[tk.Label] = None
        self.stats_x_label: Optional[tk.Label] = None
        self.stats_o_label: Optional[tk.Label] = None
        self.stats_draw_label: Optional[tk.Label] = None

        self._build_mode_selection()

    # ---------- 首頁：選擇模式 & 難度 ----------

    def _build_mode_selection(self) -> None:
        frame = tk.Frame(self.root, bg="#f4f4f8")
        frame.pack(expand=True)

        title = tk.Label(
            frame, text="OOP Tic-Tac-Toe",
            font=("Arial", 20, "bold"), bg="#f4f4f8"
        )
        title.pack(pady=(10, 20))

        label = tk.Label(frame, text="請選擇模式", font=("Arial", 14), bg="#f4f4f8")
        label.pack(pady=5)

        # 模式按鈕列
        mode_frame = tk.Frame(frame, bg="#f4f4f8")
        mode_frame.pack(pady=5)

        btn_ai_human = tk.Button(
            mode_frame, text="AI 對 人類", width=15,
            font=("Arial", 11),
            command=lambda: self._start_game("ai_vs_human")
        )
        btn_ai_human.grid(row=0, column=0, padx=5)

        btn_ai_ai = tk.Button(
            mode_frame, text="AI 對 AI", width=15,
            font=("Arial", 11),
            command=lambda: self._start_game("ai_vs_ai")
        )
        btn_ai_ai.grid(row=0, column=1, padx=5)

        # 難度選擇區
        diff_label = tk.Label(
            frame, text="請選擇難度（AI 智慧程度）", font=("Arial", 12),
            bg="#f4f4f8"
        )
        diff_label.pack(pady=(20, 5))

        diff_frame = tk.Frame(frame, bg="#f4f4f8")
        diff_frame.pack()

        rb_easy = tk.Radiobutton(
            diff_frame, text="簡單：隨機 Random",
            variable=self.difficulty_var, value="easy",
            bg="#f4f4f8"
        )
        rb_easy.pack(anchor="w")

        rb_medium = tk.Radiobutton(
            diff_frame, text="中等：規則 + 防守 Medium",
            variable=self.difficulty_var, value="medium",
            bg="#f4f4f8"
        )
        rb_medium.pack(anchor="w")

        rb_hard = tk.Radiobutton(
            diff_frame, text="困難：Minimax 最佳步",
            variable=self.difficulty_var, value="hard",
            bg="#f4f4f8"
        )
        rb_hard.pack(anchor="w")

        hint = tk.Label(
            frame,
            text="提示：難度會影響所有 AI（包含 AI 對 AI）",
            font=("Arial", 9),
            fg="#555555",
            bg="#f4f4f8"
        )
        hint.pack(pady=(15, 0))

        self.mode_frame = frame

    # ---------- 建立遊戲畫面 ----------

    def _start_game(self, mode: GameMode) -> None:
        self.mode_frame.destroy()

        # 取得目前選擇的難度（"easy" / "medium" / "hard"）
        difficulty: Difficulty = self.difficulty_var.get()  # type: ignore

        # 建立 GameManager，帶入難度
        self.manager = GameManager(mode, difficulty)
        self.manager.reset()

        # 新的一局開始，還沒記錄過結果
        self.game_recorded = False
        self.buttons = []

        # --- 外層容器 ---
        main_frame = tk.Frame(self.root, bg="#f4f4f8")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # 標題 + 模式說明列
        top_frame = tk.Frame(main_frame, bg="#f4f4f8")
        top_frame.pack(fill="x", pady=(0, 10))

        title = tk.Label(
            top_frame, text="OOP Tic-Tac-Toe",
            font=("Arial", 18, "bold"),
            bg="#f4f4f8"
        )
        title.pack(anchor="w")

        mode_text = "AI 對 人類" if mode == "ai_vs_human" else "AI 對 AI"
        diff_map = {"easy": "簡單", "medium": "中等", "hard": "困難"}
        info = tk.Label(
            top_frame,
            text=f"模式：{mode_text}   |   難度：{diff_map.get(difficulty, difficulty)}",
            font=("Arial", 10),
            fg="#555555",
            bg="#f4f4f8"
        )
        info.pack(anchor="w")

        # 狀態列
        self.status_label = tk.Label(
            main_frame, text="", font=("Arial", 14),
            bg="#f4f4f8", fg="#333333"
        )
        self.status_label.pack(pady=(5, 10))

        # 棋盤外框
        board_frame_outer = tk.Frame(main_frame, bg="#f4f4f8")
        board_frame_outer.pack(pady=5)

        board_frame = tk.Frame(board_frame_outer, bg="#dcdde1", bd=2, relief="ridge")
        board_frame.pack()

        # 3x3 棋盤按鈕
        for i in range(9):
            btn = tk.Button(
                board_frame, text=" ", font=("Arial", 26, "bold"),
                width=3, height=1,
                relief="flat",
                bg="#fefefe",
                command=lambda idx=i: self._on_cell_clicked(idx)
            )
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.buttons.append(btn)

        # 控制區：重新開始按鈕
        control_frame = tk.Frame(main_frame, bg="#f4f4f8")
        control_frame.pack(pady=(10, 5))

        reset_btn = tk.Button(
            control_frame, text="重新開始本局", command=self._reset_game,
            font=("Arial", 11),
            width=15
        )
        reset_btn.pack()

        # 分隔線
        sep = tk.Frame(main_frame, height=1, bg="#cccccc")
        sep.pack(fill="x", pady=(10, 6))

        # ===== 主畫面戰績區塊 =====
        stats_frame = tk.Frame(main_frame, bg="#f4f4f8")
        stats_frame.pack(fill="x")

        stats_title = tk.Label(
            stats_frame, text="多局戰績統計", font=("Arial", 12, "bold"),
            bg="#f4f4f8"
        )
        stats_title.grid(row=0, column=0, columnspan=2, sticky="w")

        self.stats_total_label = tk.Label(stats_frame, anchor="w", bg="#f4f4f8")
        self.stats_total_label.grid(row=1, column=0, columnspan=2, sticky="w")

        self.stats_x_label = tk.Label(stats_frame, anchor="w", bg="#f4f4f8")
        self.stats_x_label.grid(row=2, column=0, columnspan=2, sticky="w")

        self.stats_o_label = tk.Label(stats_frame, anchor="w", bg="#f4f4f8")
        self.stats_o_label.grid(row=3, column=0, columnspan=2, sticky="w")

        self.stats_draw_label = tk.Label(stats_frame, anchor="w", bg="#f4f4f8")
        self.stats_draw_label.grid(row=4, column=0, columnspan=2, sticky="w")

        self._update_ui()
        self._update_stats_labels()  # 一開始顯示目前戰績（通常都是 0）

        # 若是 AI 先手（且在 AI vs Human 模式），讓 AI 自動先走一步
        self._maybe_ai_first_move()

        # 如果是 AI 對 AI，啟動自動對戰
        if mode == "ai_vs_ai":
            self._ai_vs_ai_loop()

    # ---------- 遊戲流程 ----------

    def _reset_game(self) -> None:
        if self.manager is None:
            return
        self.manager.reset()
        # 新的一局開始，先把「這局是否已記錄」重設
        self.game_recorded = False
        self._update_ui()
        # 戰績是累積的，所以不用歸零，只要維持顯示
        self._update_stats_labels()

        # reset 後也檢查一次：是否需要讓 AI 先走一步
        self._maybe_ai_first_move()

        if self.manager.mode == "ai_vs_ai":
            self._ai_vs_ai_loop()

    def _maybe_ai_first_move(self) -> None:
        """
        如果現在是 AI 先手（且模式是 AI vs Human），
        就在一開始自動讓 AI 下第一步，不用玩家先按。
        """
        if self.manager is None or self.manager.env.done:
            return
        if self.manager.mode != "ai_vs_human":
            return
        # 如果現在輪到的不是人類 → 就是 AI 先手
        if not self.manager.is_current_player_human():
            # 稍微延遲，看起來像 AI 在思考
            self.root.after(400, self._ai_move_once)

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

    # ---------- 戰績統計邏輯（顯示在主畫面） ----------

    def _record_result(self) -> None:
        """
        把目前這一局的結果記錄進戰績（只記一次）。
        """
        if self.manager is None:
            return
        env = self.manager.env
        if not env.done:
            return
        if self.game_recorded:
            return  # 已經記過了就不要重複記

        self.game_recorded = True
        self.total_games += 1

        if env.winner == 'X':
            self.x_wins += 1
        elif env.winner == 'O':
            self.o_wins += 1
        else:
            self.draws += 1

        # 更新畫面上的統計文字
        self._update_stats_labels()

    def _update_stats_labels(self) -> None:
        """
        依照目前統計數字更新主畫面戰績 Label 的文字。
        """
        if (
            self.stats_total_label is None or
            self.stats_x_label is None or
            self.stats_o_label is None or
            self.stats_draw_label is None
        ):
            return

        total = self.total_games
        x_w = self.x_wins
        o_w = self.o_wins
        d_w = self.draws

        if total > 0:
            x_rate = x_w / total * 100
            o_rate = o_w / total * 100
            d_rate = d_w / total * 100
        else:
            x_rate = o_rate = d_rate = 0.0

        self.stats_total_label.config(
            text=f"總對局數：{total}"
        )
        self.stats_x_label.config(
            text=f"X 勝：{x_w} 局（{x_rate:.1f}%）"
        )
        self.stats_o_label.config(
            text=f"O 勝：{o_w} 局（{o_rate:.1f}%）"
        )
        self.stats_draw_label.config(
            text=f"平手：{d_w} 局（{d_rate:.1f}%）"
        )

    # ---------- UI 更新 ----------

    def _update_ui(self) -> None:
        if self.manager is None:
            return
        env = self.manager.env

        # 更新棋盤按鈕文字與可用性
        for i, btn in enumerate(self.buttons):
            value = env.board[i]
            if value is None:
                btn.config(text=" ", state="normal", fg="#000000")
            else:
                # X / O 顏色區分
                if value == 'X':
                    btn.config(text="X", fg="#0070f3", state="disabled")
                else:
                    btn.config(text="O", fg="#e84118", state="disabled")

        # 更新狀態列
        if self.status_label is None:
            return

        if env.done:
            # 一旦遊戲結束，就紀錄進戰績（只會記一次）
            self._record_result()

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