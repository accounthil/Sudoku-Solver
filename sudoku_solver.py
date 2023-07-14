import requests

#Take in list of lists to represent sudoku
#0 represents empty box

# -- later: link to api of soduko solver/generator website to self-generate sudoku
#implement gui where user can solve, and autosolve if required
grid = [[0,5,4,0,7,9,6,0,0],
        [8,0,0,0,0,0,0,5,0],
        [7,0,0,0,4,0,0,0,0],
        [0,0,0,0,0,8,0,0,1],
        [0,0,7,0,0,0,0,0,0],
        [0,4,6,0,1,0,0,2,0],
        [0,0,0,3,0,0,9,0,0],
        [5,0,0,0,0,0,0,0,0],
        [0,2,1,0,8,0,0,6,0]]

def main():
    #while True:
    global grid
    #grid = get_puzzle()
    for row in grid:
        print(row)
    print('',end="\n\n")
    grid = solve_puzzle(grid)
    for row in grid:
        print(row)
    

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

