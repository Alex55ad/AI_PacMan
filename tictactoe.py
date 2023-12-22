import tkinter as tk
from tkinter import messagebox
import subprocess

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=("Arial", 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def on_button_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner_with_mace4():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
    # Check rows, columns, and diagonals for a winner
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        for condition in win_conditions:
            if (self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]]) and \
            (self.board[condition[0]] != " "):
                return True
        return False

    def check_winner_with_mace4(self):
        mace_input = """
            op col.
            op empty.
            op cell.
            op row.

            eq X = col(X).
            eq O = col(O).
            eq E = empty(E).

            board(
                cell({}, {}, {}),
                cell({}, {}, {}),
                cell({}, {}, {})
            ).

            include win.
        """.format(*self.board)

        with open("tic_tac_toe.mace", "w") as f:
            f.write(mace_input)

        command = "mace4 -f tic_tac_toe.mace > tic_tac_toe.out"
        try:
            subprocess.run(command, shell=True, check=True)
            print("Solutions still remain!")
        except subprocess.CalledProcessError as e:
            print("No solutions left!", e)


    def reset_game(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
