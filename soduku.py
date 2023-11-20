import tkinter as tk

class SudokuGUI:
    def __init__(self, root, board):
        self.root = root
        self.root.title("Sudoku Solver")

        self.board = board

        self.grid = [[tk.Entry(root, width=2, font=('Arial', 18)) for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                value = self.board[i][j]
                if value != 0:
                    self.grid[i][j].insert(tk.END, str(value))
                    self.grid[i][j].config(state=tk.DISABLED)  # Girişleri değiştirilemez yap

                self.grid[i][j].grid(row=i, column=j)

        solve_button = tk.Button(root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, columnspan=9)

        number_buttons = [tk.Button(root, text=str(num), command=lambda n=num: self.set_number(n)) for num in range(1, 10)]
        for i, button in enumerate(number_buttons):
            button.grid(row=10, column=i)

    def validate_input(self, event):
        # Allow only digits from 1 to 9
        if event.char.isdigit() and 1 <= int(event.char) <= 9:
            event.widget.delete(0, tk.END)
            event.widget.insert(tk.END, event.char)

    def set_number(self, num):
        selected = self.root.focus_get()
        if isinstance(selected, tk.Entry):
            selected.delete(0, tk.END)
            selected.insert(tk.END, str(num))

    def solve_sudoku(self):
        for i in range(9):
            for j in range(9):
                value = self.grid[i][j].get()
                if not value.isdigit() or not 1 <= int(value) <= 9:
                    tk.messagebox.showerror("Error", "Invalid input. Please enter digits from 1 to 9.")
                    return
                self.board[i][j] = int(value)

        if self.solve():
            self.display_solution()
        else:
            tk.messagebox.showerror("Error", "No solution exists.")

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True  # Sudoku çözüldü
        row, col = empty

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0  # Eğer bu sayı işe yaramazsa geri al

        return False  # Hiçbir sayı işe yaramazsa geri dön

    def is_safe(self, row, col, num):
        # Satır kontrolü
        if num in self.board[row]:
            return False

        # Sütun kontrolü
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Küçük kare kontrolü
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def display_solution(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(tk.END, str(self.board[i][j]))
                self.grid[i][j].config(state=tk.DISABLED)  # Girişleri değiştirilemez yap


if __name__ == "__main__":
    root = tk.Tk()
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    sudoku_gui = SudokuGUI(root, sudoku_board)
    root.mainloop()
