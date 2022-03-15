class State:
    def __init__(self, grid):
        self.grid = grid
        self.empty = emptyCells(self.grid)
        self.hCost = 0

    def print(self):
        print('### state:')
        printGrid(self.grid)

#   getSquare(grid, p) : grid の添字 p のマス目を含む 3x3 の領域内の数字のリスト
def getSquare(grid, p):
    q = (p // 9) // 3
    r = (p % 9) // 3
    ret = []
    for k in range(3):
        idx = 9 * (3 * q + k) + 3 * r 
        ret.extend(grid[idx:idx+3])
    return ret

#   getRow(grid, p) : grid の添字 p のマス目を含む列の領域の数字のリスト
def getRow(grid, p):
    idx = 9 * (p // 9)
    return grid[idx:idx+9]

#   getCol(grid, p) : grid の添字 p のマス目を含む行の領域の数字のリスト
def getCol(grid, p):
    r = p % 9
    return [grid[i + r] for i in list(range(0, 81, 9))]


def printGrid(grid):
    out = '+---+---+---+'
    for i in range(9):
        out += '\n|'
        for j in range(3):
            out += ''.join([('.' if c == 0 else str(c)) for c in grid[(9*i+3*j):(9*i+3*j)+3]])
            out += '|'
        if i % 3 == 2: out += '\n+---+---+---+'
    print(out)

#   emptyCells(grid) : grid 中の空マスの位置のリスト
def emptyCells(grid):
    return [i for i, v in enumerate(grid) if v == 0]

#   readSudoku(filename) : filename から問題を読んで grid を返す
def readSudoku(filename):
    prob = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#': continue
            prob.extend([0 if v == '.' else int(v) for v in line.strip()])
    return prob
    
#   fixedNumbers(grid, p) : grid 中の位置 p に置けない数のリスト
def fixedNumbers(grid, p):
    List = []
    List.extend(getSquare(grid,p))
    List.extend(getRow(grid,p))
    List.extend(getCol(grid,p))
    nList = set(List)
    if 0 in nList:
        nList.remove(0)
    return nList

#   possibleNumbers(grid, p) : grid 中の位置 p に置ける数のリスト
def possibleNumber(grid,p):
    nonexist = [1,2,3,4,5,6,7,8,9]
    exist = fixedNumbers(grid,p)
    for l in exist:
        nonexist.remove(l)
    return nonexist

#   noViolation(grid, p) : p の位置に置いた数がルールに沿っているか？
def noViolation(grid,p):
    Rlist = getRow(grid,p)
    Clist = getCol(grid,p)
    Slist = getSquare(grid,p)
    for i in range(1,9):
        cR = Rlist.count(i)
        cC = Clist.count(i)
        cS = Slist.count(i)
        if cR > 1 or cC > 1 or cS > 1:
            return False
    return True


#与えられたstateのhコストを返す
def hCost(state):
    min = 10
    p = state
    for pp in p.empty:
        pl = possibleNumber(p.grid,pp)
        if len(pl) < min:
            min = len(pl)
            pos = pp
    return min

#与えられたstateのhコストを返す
def hCostPos(state):
    min = 10
    p = state
    for pp in p.empty:
        pl = possibleNumber(p.grid,pp)
        if len(pl) < min:
            min = len(pl)
            pos = pp
    return pos

#次にきそうな状態を返す
def nextStates(state,pos):
    stateList = []
    plist = possibleNumber(state.grid,pos)

    for v in plist:
        state.grid[pos] = v
        stateList.append(state)
    return stateList


#--------------------------------------------------------

#ヒープの一番下に値を加える
def push(frontier,i):
    frontier.append(i)
    _down(frontier,0,len(frontier)-1)

#ヒープの一番下に入った値を比較し、上げる
def _down(frontier,s_pos,pos):
    new_i = frontier[pos]
    while pos > s_pos:
        p_pos = (pos - 1) // 2
        parent = frontier[p_pos]
        if new_i.hCost < parent.hCost:
            frontier[pos] = parent
            pos = p_pos
            continue
        break
    frontier[pos] = new_i

#ヒープから最小値を取り出す
def pop(frontier):
    last = frontier.pop()
    if frontier:
        re_i = frontier[0]
        frontier[0] = last
        _up(frontier,0)
        return re_i
    return last

#ヒープ内の最小値を一番上に持ってくる
def _up(frontier,pos):
    e_pos = len(frontier)
    s_pos = pos
    new_i = frontier[pos]

    c_pos = 2*pos + 1
    while c_pos < e_pos:
        r_pos = c_pos + 1
        if r_pos < e_pos and not frontier[c_pos].hCost < frontier[r_pos].hCost:
            c_pos = r_pos
        frontier[pos] = frontier[c_pos]
        pos = c_pos
        c_pos = 2*pos + 1
    frontier[pos] = new_i
    _down(frontier,s_pos,pos)

#-----------------------------------------------------------------


if __name__ == "__main__":

    import sys

    if len(sys.argv) == 1:
        print('Usage: %s sudoku-problem-file' % sys.argv[0])
        print( ' example of file format: ')
        print( '  .........')
        print( '  ......28.')
        print( '  3764.....')
        print( '  7....1...')
        print( '  .2.......')
        print( '  4..3....6')
        print( '  .1..28...')
        print( '  .....5...')
        print( '  ........3')
        sys.exit()

    prob = readSudoku(sys.argv[1])
    start = State(prob)
    printGrid(prob)

    frontier = [start]
    explored = []

    while 1:

        #frontierが空、探索失敗
        if frontier == []:
            print("Falure")
            printGrid(explored[-1])
            break
        
        #frontierに属する空きマスの中で、Hコストが最も低いstate
        new_state = pop(frontier)
        pos = hCostPos(new_state)

        if new_state.grid in explored:
            continue
        explored.append(new_state.grid)

        #探索終了
        if new_state.empty == []:
            print("solved")
            printGrid(new_state.grid)

        #nextStatesから状態を選んでfrontierに入れる
        for ns in nextStates(new_state,pos):
            if ns.grid in explored:
                continue
            if noViolation(ns.grid,pos):
                new_state.hCost = hCost(ns)
                push(frontier,ns)

