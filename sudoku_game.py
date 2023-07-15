import tkinter as tk
import requests
from copy import deepcopy

grids =  [
        [0,5,4,0,7,9,6,0,0],
        [8,0,0,0,0,0,0,5,0],
        [7,0,0,0,4,0,0,0,0],
        [0,0,0,0,0,8,0,0,1],
        [0,0,7,0,0,0,0,0,0],
        [0,4,6,0,1,0,0,2,0],
        [0,0,0,3,0,0,9,0,0],
        [5,0,0,0,0,0,0,0,0],
        [0,2,1,0,8,0,0,6,0]
        ]
grid = []
input_grid = []
unsolved_grid = []


def main():
    global grid
    global input_grid
    global unsolved_grid

    grid = get_puzzle()
    input_grid = deepcopy(grid)
    unsolved_grid = deepcopy(grid)
    root = tk.Tk()
    constructor(root)
    #if solve button clicked in constructor, then
    #check_clicked will activate, which uses compare_solutions
    #to check if entries match grid after solve_puzzle has run


def compare_solutions(entries):
    global grid
    global input_grid
    global unsolved_grid

    count = 0
    for i in range(9):
        for j in range(9):
            if unsolved_grid[i][j] == 0:
                if entries[count] != '':
                    input_grid[i][j] = int(entries[count])
                count += 1
    solve_puzzle(grid)
    for i in range(9):
        for j in range(9):
            if input_grid[i][j] != grid[i][j]:
                return False
    return True


def check_clicked(root, entries):
    if compare_solutions(entries):
        lb = tk.Label(root, text = "YOU WON!", font = ('Arial',20))
        lb.grid(row = 20, column = 3, columnspan = 5)
    else:
        lb = tk.Label(root, text = "YOU LOST :(", font = ('Arial',20))
        lb.grid(row = 20, column = 3, columnspan = 5)


def solve_clicked(root, entries):
    #converting list of entry objects to list of ints and submitting to compare_solutions
    #to ensure that function does not run if puzzle is already solved
    if compare_solutions(list(map(lambda entry: entry.get(), entries))):
        return
    #iterating through puzzle, and if an entry is wrong, correct number is inserted
    count = 0
    for i in range(9):
        for j in range(9):
            if unsolved_grid[i][j] == 0:
                if input_grid[i][j] != grid[i][j]:
                    entries[count].insert(tk.END, grid[i][j])
                count += 1
    return


#constructor function creates GUI and fetches entries of user when solve is clicked.
def constructor(root):
    root.title("Sudoku Solver")
    root.geometry("600x500")
    entries = []
    for i in range(9):
        for j in range(11):
            if j == 8:
                pass
            if j == 3 or j == 7:
                label = tk. Label(root, text = "|", font = ('Arial',20))
                label.grid(row = i*2, column = j, sticky = "nsew")
            elif j==0:
                if grid[i][j] == 0:
                    txb = tk.Entry(root, width = 1, font = ('Arial',20), relief="ridge", justify='center')
                    txb.grid(row = i*2, column = j, sticky = "nsew", padx = (70,0))
                    entries.append(txb)
                else:
                    label = tk.Label(root, text = str(grid[i][j]), font = ('Arial',20))
                    label.grid(row = i*2, column = j, sticky = "nsew", padx = (70,0))
            elif j == 1 or j == 2:
                if grid[i][j] == 0:
                    txb = tk.Entry(root, width = 1, font = ('Arial',20), relief="ridge", justify='center')
                    txb.grid(row = i*2, column = j, sticky = "nsew")
                    entries.append(txb)
                else:
                    label = tk.Label(root, text = str(grid[i][j]), font = ('Arial',20))
                    label.grid(row = i*2, column = j, sticky = "nsew")
            elif grid[i][j-(j//4)] == 0:
                txb = tk.Entry(root, width = 1, font = ('Arial',20), relief="ridge", justify='center')
                txb.grid(row = i*2, column = j, sticky = "nsew")
                entries.append(txb)
            else:
                label = tk.Label(root, text = str(grid[i][j-(j//4)]) + "", font = ('Arial',20))
                label.grid(row = i*2, column = j, sticky = "nsew")
        if i == 5 or i == 2:
            lab = tk.Label(root, text = "--------------+-----------------+---------------", font = ('Arial',20))
            lab.grid(row = i*2+1, column = 0, columnspan = 11, sticky = "nsew", padx = (70,0))
    
    def temp():
        list_of_entries = list(map(lambda entry: entry.get(), entries))
        check_clicked(root, list_of_entries)

    #button to check whether grid is correct
    check = tk.Button(root, text = "check", command = temp)
    check.grid(row = 20, column = 8, columnspan=4)

    #button for computer to solve
    button = tk.Button(root, text = "computer solve", command = lambda:solve_clicked(root,entries))
    button.grid(row = 20, column = 3, columnspan=4)
    root.mainloop()


def solve_puzzle(grid):
    #takes in the grid and solves, returning true if possible and false if not
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                continue
            for num in range(1,10):
                if check(grid, row, col, num):
                    #print(f"{row}, {col}")
                    grid[row][col] = num
                    if solve_puzzle(grid) != False:
                        return grid
                    grid[row][col] = 0
            return False
    return grid


def check(grid, row, column, num):
    """
    takes in the grid, row and column of box we are checking,
    and number that we are testing
    """
    #check if its the row
    if num in grid[row]:
        return False

    #check if its the column
    for i in range(9):
        if grid[i][column] == num:
            return False

    #check if its in the square
    r = (row // 3) * 3
    c = (column//3) * 3
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            if grid[i][j] == num:
                return False
    return True


def get_puzzle():
    url = "https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:2){grids{value,difficulty}}}"

    response = requests.get(url)
    puzzle = response.json()
    grid = puzzle['newboard']['grids'][0]['value']
    print(puzzle['newboard']['grids'][0]['difficulty'])
    return grid


if __name__ == "__main__":
    main()