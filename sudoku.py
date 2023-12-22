import random
import tkinter as tk
import subprocess

def solve_sudoku(grid_entries):
    sudoku_logic = [
        "assign(domain_size, 9).",      
        "assign(max_seconds, 2).",      
        "formulas(sudoku_rules).",
        "all x all y1 all y2 (f(x, y1) = f(x, y2) -> y1 = y2).",
        "all x1 all x2 all y (f(x1, y) = f(x2, y) -> x1 = x2).",
        "all x same_interval(x,x).",
        "all x all y (same_interval(x,y) -> same_interval(y,x)).",
        "all x all y all z (same_interval(x,y) & same_interval(y,z) -> same_interval(x,z)).",
        "same_interval(0,1). same_interval(1,2).",
        "same_interval(3,4). same_interval(4,5).",
        "same_interval(6,7). same_interval(7,8).",
        "-same_interval(0,3). -same_interval(3,6). -same_interval(0,6).",
        "all x1 all y1 all x2 all y2",
        "  (same_interval(x1,x2) & same_interval(y1,y2) & f(x1, y1) = f(x2, y2)",
        "  -> x1 = x2 & y1 = y2 ).",
        "all x all z exists y (f(x,y) = z).",
        "all y all z exists x (f(x,y) = z).",
        "end_of_list.",
        "formulas(sample_puzzle)."
    ]

    # Extract numbers from the grid_entries and write to the puzzle rules
    for i, row in enumerate(grid_entries):
        for j, entry in enumerate(row):
            number = entry.get()
            if number != '': 
                sudoku_logic.append(f"f({i},{j}) = {number}.")

    sudoku_logic.append("end_of_list.")

    with open("sudoku.in", "w") as file:
        file.write("\n".join(sudoku_logic))

    # Run Mace4 to check solvability
    command = "mace4 -f sudoku.in > sudoku.out"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Sudoku puzzle is solvable!")
    except subprocess.CalledProcessError as e:
        print("Sudoku puzzle is not solvable!:", e)

sample_solution = [
    [5, 3, 4, 6, 7, 8, 0, 1, 2],
    [6, 7, 2, 1, 0, 5, 3, 4, 8],
    [1, 0, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 0, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 0, 1],
    [7, 1, 3, 0, 2, 4, 8, 5, 6],
    [0, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 0, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 0]
]

def fill_sample(entries):
    # Fill the grid with the sample solution
    for i in range(9):
        for j in range(9):
            number = sample_solution[i][j]
            entries[i][j].delete(0, tk.END)  # Clear any existing content
            entries[i][j].insert(tk.END, str(number))

def fill_random(entries):
    # Generate random numbers and fill the grid
    for i in range(9):
        for j in range(9):
            number = random.randint(0, 8) 
            entries[i][j].delete(0, tk.END)  # Clear any existing content
            entries[i][j].insert(tk.END, str(number)) 

def create_gui():
    root = tk.Tk()
    root.title("Sudoku Solver")

    entries = [] 

    def on_click(row, col):
        print("Clicked cell:", row, col)
       
    for i in range(9):
        entry_row = []
        for j in range(9):
            cell = tk.Entry(root, width=5)
            cell.grid(row=i, column=j)
            cell.bind('<Button-1>', lambda e, row=i, col=j: on_click(row, col))
            entry_row.append(cell)
        entries.append(entry_row)

        solve_button = tk.Button(root, text="Mace4 proof", command=lambda: solve_sudoku(entries))
    solve_button.grid(row=10, column=4, columnspan=2)

    fill_button = tk.Button(root, text="Fill Random", command=lambda: fill_random(entries))
    fill_button.grid(row=10, column=0, columnspan=2)

    sample_button = tk.Button(root, text="Fill Sample", command=lambda: fill_sample(entries))
    sample_button.grid(row=10, column=2, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    create_gui()