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

    print("row penalty:", row_penalty)
    print("col penalty:", col_penalty)

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

print("\nInitial Basic Feasible allocation:\n")
for i in range(n):
    for j in range(m):
        print(alloc[i][j], end='\t')
    print()
print()

print("\nTransportation Allocation")
for i in range(n):
    for j in range(m):
        if alloc[i][j] > 0:
            print(alloc[i][j], "units from Warehouse ", i+1, " to Store ", j+1)

print("\nTotal cost of transportation = ", total_cost)

if no_alloc < n+m-1:
    print("\nDegenerate allocation\n")
else:
    print("\nNon-Degenerate allocation\n")
