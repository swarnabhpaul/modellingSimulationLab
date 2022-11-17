import numpy as np


def get_min_min2(array):
    m1, m2 = np.inf, np.inf
    for val in array:
        if val <= m1:
            m1, m2 = val, m1
        elif val <= m2:
            m2 = val
    return m1, m2


def get_max_penalty(array, n, m):
    row_penalty = []
    for r in range(n):
        m1, m2 = get_min_min2(array[r])
        if m1 != np.inf and m2 != np.inf:
            row_penalty.append((m2-m1, r))
        elif m1 != np.inf:
            row_penalty.append((m1, r))

    col_penalty = []
    for c in range(m):
        col_m = []
        for i in range(n):
            col_m.append(array[i][c])
        m1, m2 = get_min_min2(col_m)
        if m1 != np.inf and m2 != np.inf:
            col_penalty.append((m2-m1, c))
        elif m1 != np.inf:
            col_penalty.append((m1, c))

    print("row penalty (p, row):", row_penalty)
    print("row penalty (p, col):", col_penalty)

    if not (row_penalty or col_penalty):
        return -1, -1, None

    r_mp, c_mp = max(row_penalty), max(col_penalty)
    if r_mp > c_mp:
        i = r_mp[1]
        mp = r_mp[0]
        j = 0
        mn = array[i][j]
        for c in range(m):
            if array[i][c] < mn:
                j = c
                mn = array[i][c]
    else:
        j = c_mp[1]
        mp = c_mp[0]
        i = 0
        mn = array[i][j]
        for r in range(n):
            if array[r][j] < mn:
                i = r
                mn = array[i][c]
    return i, j, mp


def isNotClosedLoop(array):
    m, n = len(array), len(array[0])
    e_Rows = [0]*m
    e_Cols = [0]*n

    while True:
        flag = 0
        for i in range(m):
            if e_Rows[i] == 0:
                temp = []
                for j in range(n):
                    if (e_Cols[j] == 0 and array[i][j] != 0):
                        temp.append(array[i][j])
                if len(temp) < 2:
                    e_Rows[i] = 1
                    flag = 1

        for j in range(len(array[0])):
            if e_Cols[j] == 0:
                temp = []
                for i in range(m):
                    if (e_Rows[i] == 0 and array[i][j] != 0):
                        temp.append(array[i][j])
                if len(temp) < 2:
                    e_Cols[j] = 1
                    flag = 1

        if flag == 0:
            if 0 not in e_Rows and 0 not in e_Cols:
                return True
            else:
                return False


def index_min(array):
    p, q = -1, -1
    minimum = np.inf
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] < minimum:
                minimum = array[i][j]
                p = i
                q = j
    return p, q


def removeDegeneracy(alloc, C):
    n = len(C)
    m = len(C[0])

    unalloc = []
    for k in range(n):
        temp = [0]*m
        unalloc.append(temp)

    for i in range(n):
        for j in range(m):
            if int(alloc[i][j]) == int(0):
                unalloc[i][j] = C[i][j]
            else:
                unalloc[i][j] = np.inf

    i, j = index_min(unalloc)

    while i != -1 and j != -1:
        alloc[i][j] = 0.00001

        if isNotClosedLoop(alloc):
            return alloc
        else:
            alloc[i][j] = 0
            unalloc[i][j] = np.inf

        i, j = index_min(unalloc)
    return alloc


S = []
D = []
C = []
sum_D, sum_S, total_cost, no_alloc = 0, 0, 0, 0

n = int(input("Number of Warehouses : "))
m = int(input("Number of Stores : "))

S = list(map(int, input("Supply matrix : ").strip().split()))[:n]
D = list(map(int, input("Demand matrix : ").strip().split()))[:m]

print("Cost matrix : ")
for i in range(n):
    r = list(map(int, input().strip().split()))[:m]
    C.append(r)

c_m = []
for i in range(n):
    c_m.append([0]*m)
    for j in range(m):
        c_m[i][j] = C[i][j]

sum_S = sum(S)
sum_D = sum(D)

if (sum_S == sum_D):
    print("\nBalanced Problem\n")
else:
    print("\nNot Balanced Problem. Making it balanced\n")
    if sum_S < sum_D:
        C = np.append(C, np.array(np.zeros((1, m))), axis=0)
        S = np.append(S, sum_D-sum_S)
        n += 1
    elif sum_S > sum_D:
        cost = np.concatenate((C, np.zeros((n, 1))), axis=1)
        demand = np.append(D, sum_S-sum_D)
        m += 1
    print("\nProblem is now Balanced Problem\n")

alloc = []
for k in range(n):
    temp = [0]*m
    alloc.append(temp)

i, j, max_penalty = get_max_penalty(C, n, m)
while (max_penalty != None):
    print("selected for allocation, i=", i, " j=", j)

    x = min(S[i], D[j])
    S[i] = S[i] - x
    D[j] = D[j] - x

    if x > 0:
        no_alloc = no_alloc + 1
        total_cost = total_cost + x*C[i][j]
        alloc[i][j] = x
    if S[i] == 0:
        for j in range(m):
            C[i][j] = np.inf
    if D[j] == 0:
        for i in range(n):
            C[i][j] = np.inf

    i, j, max_penalty = get_max_penalty(C, n, m)

print("\nTransportation Allocation")
for i in range(n):
    for j in range(m):
        if alloc[i][j] > 0:
            print(alloc[i][j], "units from Warehouse ", i+1, " to Store ", j+1)

print("\nTotal cost of transportation = ", total_cost)

if no_alloc < n+m-1:
    print("\nDegenerate allocation Removing Degeneracy")
    alloc = removeDegeneracy(alloc, c_m)

    print("\nInitial Basic Feasible allocation\n")
    for i in range(n):
        for j in range(m):
            print(alloc[i][j], end='\t')
        print()
    print()
else:
    print("\nNon-Degenerate alloc \n")
