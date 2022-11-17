import numpy as np
from collections import defaultdict


class Transportation_Problem:
    def __init__(self, C, S, D):
        self.C = np.array(C).astype(float)  # cost matrix
        self.S = np.array(S).astype(float)  # supply matrix
        self.D = np.array(D).astype(float)  # demand matrix
        self.A = np.zeros(self.C.shape).astype(float)  # allocation matrix
        self.total_cost = 0
        self.no_alloc = 0
        self.total_demand = 0
        self.total_supply = 0
        self.rows, self.cols = self.C.shape
        self.u, self.v, self.delta = None, None, None

    def is_balanced(self):
        self.total_demand = np.sum(self.D)
        self.total_supply = np.sum(self.S)
        return self.total_demand == self.total_supply

    def make_balanced(self):
        if self.total_demand < self.total_supply:
            self.D = np.append(self.D, np.array([self.total_supply-self.total_demand]))
            self.C = np.append(self.C, np.zeros((self.rows, 1)), axis=1)
            self.total_demand = np.sum(self.D)
            self.rows, self.cols = self.C.shape
        elif self.total_demand > self.total_supply:
            self.S = np.append(self.S, np.array([self.total_demand-self.total_supply]))
            self.C = np.append(self.C, np.zeros((1, self.cols)), axis=0)
            self.total_supply = np.sum(self.S)
            self.rows, self.cols = self.C.shape

    def is_degenerate(self):
        return (self.rows+self.cols-1) == self.no_alloc

    def make_non_degenerate(self, d=0.001):

        def is_independent(A):
            # eliminate rows and cols
            r, c = A.shape
            rows = list(range(r))
            cols = list(range(c))
            flag = True
            while flag:
                flag = False
                for r in rows[:]:
                    if np.count_nonzero(A[r, cols]) < 2:
                        rows.remove(r)
                        flag = True
                for c in cols[:]:
                    if np.count_nonzero(A[rows, c]) < 2:
                        cols.remove(c)
                        flag = True
            return not (len(rows) > 0 and len(cols) > 0)

        diff = (self.rows+self.cols-1) - self.no_alloc
        empty_cells = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.A[r][c] == 0:
                    empty_cells.append((self.C[r][c], r, c))
        empty_cells.sort()
        for i in range(diff):
            while empty_cells:
                _, r, c = empty_cells[0]
                empty_cells.pop(0)
                A = self.A.copy()
                A[r, c] = d
                if is_independent(A):
                    self.A[r, c] = d
                    break
            else:
                print("Warning : couldn't fix degeneracy")

    def recalculate_cost(self):
        self.total_cost = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.total_cost += self.C[i, j]*self.A[i, j]

    def north_west_corner(self):
        cm = self.C.copy()
        r, c = self.C.shape
        D = self.D.copy()
        S = self.S.copy()
        self.A = np.zeros(self.C.shape).astype(float)
        total_cost, no_alloc = 0, 0
        i = 0
        j = 0
        while (i < r) and (j < c):
            x = min(D[j], S[i])
            D[j] -= x
            S[i] -= x
            total_cost += x * cm[i, j]
            no_alloc += 1
            self.A[i, j] = x
            if D[j] < S[i]:
                j += 1
            elif D[j] > S[i]:
                i += 1
            else:
                i += 1
                j += 1
        self.total_cost = total_cost
        self.no_alloc = no_alloc

    def least_cost(self):

        def get_min_cost(C):
            i, j, min_cost = 0, 0, C[0][0]
            for m in range(C.shape[0]):
                for n in range(C.shape[1]):
                    if C[m, n] < min_cost:
                        i, j, min_cost = m, n, C[m, n]
            return i, j, min_cost

        C, S, D = self.C.copy(), self.S.copy(), self.D.copy()
        self.A = np.zeros(self.C.shape).astype(float)
        r, c = self.C.shape
        self.total_cost = 0
        self.no_alloc = 0

        i, j, min_cost = get_min_cost(C)
        while min_cost != np.inf:
            x = min(S[i], D[j])
            S[i] -= x
            D[j] -= x
            self.total_cost += x*C[i, j]
            self.no_alloc += 1
            self.A[i, j] = x
            if S[i] <= D[j]:
                for k in range(c):
                    C[i, k] = np.inf
            if S[i] >= D[j]:
                for k in range(r):
                    C[k, j] = np.inf

            i, j, min_cost = get_min_cost(C)

    def vogel_approximation(self):
        def get_min_min2(M):
            m1, m2 = np.inf, np.inf
            for m in M:
                if m <= m1:
                    m1, m2 = m, m1
                elif m <= m2:
                    m2 = m
            return m1, m2

        def get_max_penalty(C):
            row_penalty = {}
            for r in range(C.shape[0]):
                m1, m2 = get_min_min2(C[r, :])
                if m1 != np.inf and m2 != np.inf:
                    row_penalty[r] = m2-m1
                elif m1 != np.inf:
                    row_penalty[r] = m1

            col_penalty = {}
            for c in range(C.shape[1]):
                m1, m2 = get_min_min2(C[:, c])
                if m1 != np.inf and m2 != np.inf:
                    col_penalty[c] = m2-m1
                elif m1 != np.inf:
                    col_penalty[c] = m1

            print("row penalty :", " ".join([str(row_penalty[i]) if i in row_penalty else "-" for i in range(C.shape[0])]))
            print("col penalty :", " ".join([str(col_penalty[i]) if i in col_penalty else "-" for i in range(C.shape[1])]))

            if not (row_penalty or col_penalty):
                return -1, -1, None

            r_mp, c_mp = max(row_penalty, key=lambda x: row_penalty[x]), max(col_penalty, key=lambda x: col_penalty[x])
            if r_mp > c_mp:
                i, mp = r_mp, row_penalty[r_mp]
                j = 0
                mn = C[i, j]
                for c in range(C.shape[1]):
                    if C[i, c] < mn:
                        j = c
                        mn = C[i, c]
            else:
                j, mp = c_mp, col_penalty[c_mp]
                i = 0
                mn = C[i, j]
                for r in range(C.shape[0]):
                    if C[r, j] < mn:
                        i = r
                        mn = C[r, j]

            return i, j, mp

        C, S, D = self.C.copy(), self.S.copy(), self.D.copy()
        self.A = np.zeros(self.C.shape).astype(float)
        r, c = self.C.shape
        self.total_cost = 0
        self.no_alloc = 0

        count = 1
        print(f"\nP{count}")
        count += 1
        i, j, max_penalty = get_max_penalty(C)
        while max_penalty != None:
            print(f"row = S{i+1} col = D{j+1} max penalty = {max_penalty}")
            x = min(S[i], D[j])
            S[i] -= x
            D[j] -= x
            self.total_cost += x*C[i, j]
            self.no_alloc += 1
            self.A[i, j] = x
            if S[i] <= D[j]:
                for k in range(c):
                    C[i, k] = np.inf
            if S[i] >= D[j]:
                for k in range(r):
                    C[k, j] = np.inf
            print(f"\nP{count}")
            count += 1
            i, j, max_penalty = get_max_penalty(C)

    def is_optimal(self):
        max_row_alloc_count, row = max([(np.count_nonzero(self.A[r, :]), r) for r in range(self.rows)])
        max_col_alloc_count, col = max([(np.count_nonzero(self.A[:, c]), c) for c in range(self.cols)])
        u = np.zeros((self.rows))
        v = np.zeros((self.cols))

        if max_row_alloc_count < max_col_alloc_count:
            s = ('v', col)
            v[col] = 0
            print(f"substituting v{col}=0, we get,")
        else:
            s = ('u', row)
            u[row] = 0
            print(f"substituting u{row}=0, we get,")

        # bfs
        visited = set()
        q = [s]
        while q:
            flag, index = q[0]
            if q[0] not in visited:
                if flag == 'u':
                    for i, a in enumerate(self.A[index, :]):
                        if a != 0:
                            v[i] = self.C[index][i]-u[index]
                            if ('v', i) not in visited:
                                print(f"u{index}={u[index]} --> v{i}={v[i]},")
                            q.append(('v', i))
                else:
                    for i, a in enumerate(self.A[:, index]):
                        if a != 0:
                            u[i] = self.C[i][index]-v[index]
                            if ('u', i) not in visited:
                                print(f"v{index}={v[index]} --> u{i}={u[i]},")
                            q.append(('u', i))

            visited.add(q[0])
            q.pop(0)

        print("u = ", u, " v = ", v)

        delta = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                delta[i][j] = self.C[i][j]-u[i]-v[j]

        self.u, self.v, self.delta = u, v, delta
        print("delta :\n", delta)
        return not (np.any(delta < 0))

    def modi(self):
        # give min delta a value
        min_del_i, min_del_j = np.unravel_index(np.argmin(self.delta, axis=None), self.delta.shape)
        A = self.A.copy()
        A[min_del_i, min_del_j] = 0.00001

        # eliminate rows and cols
        rows = list(range(self.rows))
        cols = list(range(self.cols))
        flag = True
        while flag:
            flag = False
            for r in rows[:]:
                if np.count_nonzero(A[r, cols]) < 2:
                    rows.remove(r)
                    flag = True
            for c in cols[:]:
                if np.count_nonzero(A[rows, c]) < 2:
                    cols.remove(c)
                    flag = True

        # find all valid allocations for creating path
        allocs = []
        for r in rows:
            for c in cols:
                if A[r, c] != 0:
                    allocs.append((r, c))

        # find the closed path
        path = [(min_del_i, min_del_j)]
        if (min_del_i, min_del_j) in allocs:
            allocs.remove((min_del_i, min_del_j))
        while allocs:
            last_i, last_j = path[-1]
            min_i, min_j = np.inf, np.inf
            for i, j in allocs:
                if i == last_i and abs(j-last_j) < abs(min_j-last_j):
                    min_i, min_j = i, j
                elif j == last_j and abs(i-last_i) < abs(min_i-last_i):
                    min_i, min_j = i, j
            path.append((min_i, min_j))
            allocs.remove((min_i, min_j))
        print("closed path: ", " -> ".join([f"S{i+1}D{j+1}" for i, j in path]))
        # find minimum at negetive position
        negs = [self.A[path[i][0], path[i][1]] for i in range(1, len(path), 2)]
        min_neg = min(negs)
        for i in range(len(path)):
            if i % 2 == 0:
                self.A[path[i][0], path[i][1]] += min_neg
            else:
                self.A[path[i][0], path[i][1]] -= min_neg
        self.no_alloc = np.count_nonzero(self.A != 0)

    def solve(self, initial_sol_func):
        print("Cost Matrix:\n", self.C)
        print("Supply Matrix:\n", self.S)
        print("Demand Matrix:\n", self.D)
        if self.is_balanced():
            print("Balanced Transportation Problem.")
        else:
            print("Unbalanced Transportation Problem")
        print()

        initial_sol_func()
        print("Initial basic feasible solution:")
        print("Total Cost: ", self.total_cost)
        print()
        print("No of Allocation: ", self.no_alloc)
        print()
        print("Allocations:\n", self.A)
        if self.is_degenerate() and self.is_balanced():
            print("It is not a Degenerate Solution")
        else:
            print("Degenerate Solution")
            print("allotting dummy allocations ... ")
            tp.make_non_degenerate()
            print("\nNew Allocations:\n", tp.A)
        print()
        print("Checking optimality:")
        while not tp.is_optimal():
            print("\nThe given allocations are not optimal.")
            print("applying modi optimization: ")
            tp.modi()
            if self.is_degenerate() and self.is_balanced():
                print("It is not a Degenerate Solution")
            else:
                print("Degenerate Solution")
                print("allotting dummy allocations ... ")
                tp.make_non_degenerate()
            print()

            print("\nNew Allocations:\n", tp.A)
            tp.recalculate_cost()
            print("Total cost: ", tp.total_cost)
            print()
            print("Checking optimality:")
        print("\nThe allocations are optimal.")
        print()
        print("Final allocations:\n", tp.A)
        print("Final minimimum cost:", tp.total_cost)


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    s = int(input("Enter number of supply :"))
    d = int(input("Enter number of demand :"))
    print("Enter the cost matrix:")
    C = [list(map(int, input().split())) for _ in range(s)]
    print("Enter the supply matrix:")
    S = list(map(int, input().split()))
    print("Enter the demand matrix:")
    D = list(map(int, input().split()))
    tp = Transportation_Problem(C, S, D)
    tp.solve(initial_sol_func=tp.least_cost)

# Input
# 3
# 4
# 21 16 25 13
# 17 18 14 23
# 32 17 18 41

# Supply matrix
# 11 13 19

# Demand matrix
# 6 10 12 15
