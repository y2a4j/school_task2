#8パズル

class State:

    def __init__(self,puzzle):
        self.puzzle = puzzle
        self.idx = 0
        self.gCost = 0
        self.hCost = 0
        self.fCost = self.gCost + self.hCost
        self.prev = None

    #ゴールかどうか
    def isGoal(self):
        if self.puzzle == '12345678.':
            return True
        return False

    #空白の位置の取得
    def whBrank(self):
        for i,p in enumerate(self.puzzle):
            if p == '.':
                return i

    #ｈコスト
    def HCost(self):
        return 0

    #次に進める位置のリスト
    def nextStates(self):
        nlist = []
        idx = State.whBrank(self)
        if idx == 0:
            ilist = [1,3]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 1:
            ilist = [0,2,4]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 2:
            ilist = [1,5]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 3:
            ilist = [0,4,6]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 4:
            ilist = [1,3,5,7]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 5:
            ilist = [2,4,8]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 6:
            ilist = [3,7]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 7:
            ilist = [4,6,8]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist
        if idx == 8:
            ilist = [5,7]
            for ns_idx in ilist:
                ns = State(State.strSwap(self.puzzle,idx,ns_idx))
                nlist.append(ns)
            return nlist

    #0<=i,j<len(str)のとき
    #位置iと位置jの文字を交換した文字列を返す
    def strSwap(str,i,j):
        if i > j: 
            i, j = j, i
        return str[:i] + str[j] + str[i+1:j] + str[i] + str[j+1:]


#---------------------------------------------------------
#リストソート

def push(frontier,state):
    frontier.insert(0,state)
    sort(frontier,len(frontier))

def sort(list,l):
    for right in range(1,l):
        key = list[right]
        left = right
        while left > 0 and key.fCost < list[left - 1].fCost:
            list[left] = list[left - 1]
            left -= 1
        list[left] = key

def pop(frontier):
    last = frontier[0]
    frontier.remove(last)
    return last

#---------------------------------------------------------


if __name__ == "__main__":

    import sys
    import time

    #入力ミスのエラー表示
    if len(sys.argv) <= 1:
        print("Usage: %s 8puzzle" % sys.argv[0])
        sys.exit(1)
    if len(sys.argv[1]) != 9:
        print("is not 8 puzzle")
        sys.exit(1)

    start = State(sys.argv[1])
    frontier = []
    push(frontier,start)
    explored = []

    t1 = time.time()

    while 1:
        #frontierが空、探索失敗
        if frontier == []:
            print("Goal not found")
            print("trials: %s " ,explored)
            break

        #frontierに属するfコスト最小の節点
        s = pop(frontier)

        if s.puzzle in explored:
            continue
        explored.append(s.puzzle)

        #ゴールかどうか
        if State.isGoal(s):
            t2 = time.time()
            print("Goal found")
            result = []
            prev = s
            while prev is not None:
                result.insert(0,prev.puzzle)
                prev = prev.prev
            print(f"Number of trials: {len(result) - 1}")
            print(f"elapsed_time: {t2 - t1}")
            print(f"path = {result}")
            break

        #frontierに次になりそうな文字列を渡す
        for ns in State.nextStates(s):
            if ns.puzzle in explored:
                continue
            ns.prev = s
            ns.gCost = s.gCost + 1
            ns.fCost = ns.gCost + State.HCost(ns)
            push(frontier,ns)
