import time
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from typing import List, Tuple, Optional

class TicTacToeAI:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.current_player = 1  # X
        self.ai_player = 2       # O
        self.human_player = 1
        self.game_over = False
        self.ai_thinking = False
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe AI")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0)

        title_label = ttk.Label(main_frame, text="Tic-Tac-Toe AI", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        self.status_label = ttk.Label(main_frame, text="Your turn (X)", font=('Arial', 12))
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        board_frame = ttk.Frame(main_frame)
        board_frame.grid(row=2, column=0, columnspan=3)

        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(board_frame, text="", font=('Arial', 20, 'bold'), width=4, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(10, 10))

        new_game_btn = ttk.Button(control_frame, text="New Game", command=self.new_game)
        new_game_btn.grid(row=0, column=0, padx=5)

        reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_game)
        reset_btn.grid(row=0, column=1, padx=5)

        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        instructions = ttk.Label(info_frame,
                                 text="Click on any empty cell to make your move.\nYou play as X, AI plays as O.",
                                 font=('Arial', 10), justify=tk.CENTER)
        instructions.grid(row=0, column=0, pady=10)

        self.root.mainloop()

    def on_button_click(self, row, col):
        if self.game_over or self.ai_thinking:
            return

        if self.current_player == self.human_player and self.is_valid_move(row, col):
            self.make_move(row, col, self.human_player)
            self.update_button(row, col, "X")
            self.current_player = self.ai_player

            if not self.check_game_over():
                self.ai_thinking = True
                self.status_label.config(text="🤖 AI is thinking...")
                self.root.update()
                threading.Thread(target=self.make_ai_move, daemon=True).start()

    def make_ai_move(self):
        start_time = time.time()
        row, col = self.get_ai_move()
        self.root.after(0, lambda: self.complete_ai_move(row, col, start_time))

    def complete_ai_move(self, row, col, start_time):
        end_time = time.time()
        self.make_move(row, col, self.ai_player)
        self.update_button(row, col, "O")
        self.current_player = self.human_player
        self.ai_thinking = False

        thinking_time = end_time - start_time
        self.status_label.config(text=f"AI took {thinking_time:.2f}s")

        self.check_game_over()

    def update_button(self, row, col, symbol):
        btn = self.buttons[row][col]
        btn.config(text=symbol, state=tk.DISABLED)
        if symbol == "X":
            btn.config(bg="#ffcccc", fg="#cc0000")
        else:
            btn.config(bg="#ccffcc", fg="#006600")

    def check_game_over(self) -> bool:
        winner = self.check_winner()
        if winner:
            self.game_over = True
            msg = "🎉 You won!" if winner == self.human_player else "🤖 AI wins!"
            messagebox.showinfo("Game Over", msg)
            self.status_label.config(text=msg)
            return True

        if self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Game Over", "🤝 It's a tie!")
            self.status_label.config(text="It's a tie!")
            return True
        return False

    def new_game(self):
        self.reset_game()
        self.game_over = False
        self.status_label.config(text="Your turn (X)")

    def reset_game(self):
        self.board = [[0] * 3 for _ in range(3)]
        self.current_player = 1
        self.game_over = False
        self.ai_thinking = False

        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(text="", state=tk.NORMAL, bg="SystemButtonFace", fg="black")

        self.status_label.config(text="Your turn (X)")

    def is_valid_move(self, row, col):
        return self.board[row][col] == 0

    def make_move(self, row, col, player):
        self.board[row][col] = player

    def check_winner(self) -> Optional[int]:
        for row in self.board:
            if row[0] == row[1] == row[2] != 0:
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        return None

    def is_board_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def get_available_moves(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]

    def evaluate_board(self):
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        return 0

    def minimax(self, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[int, int]]]:
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10.0 - depth, None
        elif winner == self.human_player:
            return depth - 10.0, None
        elif self.is_board_full():
            return 0.0, None

        if maximizing:
            max_eval = float('-inf')
            best_move = None
            for r, c in self.get_available_moves():
                self.board[r][c] = self.ai_player
                eval, _ = self.minimax(depth + 1, alpha, beta, False)
                self.board[r][c] = 0
                if eval > max_eval:
                    max_eval, best_move = eval, (r, c)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for r, c in self.get_available_moves():
                self.board[r][c] = self.human_player
                eval, _ = self.minimax(depth + 1, alpha, beta, True)
                self.board[r][c] = 0
                if eval < min_eval:
                    min_eval, best_move = eval, (r, c)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_ai_move(self) -> Tuple[int, int]:
        _, best_move = self.minimax(0, float('-inf'), float('inf'), True)
        return best_move if best_move else self.get_available_moves()[0]

# Run the GUI
if __name__ == "__main__":
    TicTacToeAI()
