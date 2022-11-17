import numpy as np
total_cost = 0
no_alloc = 0
# taking input
r = int(input("Enter the number of rows:"))
c = int(input("\nEnter the number of columns:"))
print("\nEnter the entries in a single line (separated by space):\n")
entries = list(map(int, input().split()))
cm = np.array(entries).reshape(r, c)
print("\nCost Matrix")
print(cm)
print("\nRows, Columns: (", r, ",", c, ")")
print("\nEnter Demand values: ")
entries = list(map(int, input().split()))
print("\nDemand Matrix: ")
print(entries)
cm = np.insert(cm, [r], [entries], axis=0)
r += 1
print("\nEnter Supply values: ")
entries = list(map(int, input().split()))
print("\nSupply Matrix: ", sep='')
print(entries)
entries.append(0)
cm = np.insert(cm, [c], np.array([entries]).transpose(), axis=1)
c += 1
print("\nModified Cost Matrix: ")
print(cm)
total_demand = np.sum(cm[r-1, :])
total_supply = np.sum(cm[:, c-1])
if total_demand == total_supply:
    print("\nBalanced Transportation Problem.")
else:
    print("\nUnbalanced Transportation Problem")
    # Add dummy row/column
    if total_demand < total_supply:
        cm = np.insert(cm, c-1, 0, axis=1)
        cm[r-1][c-1] = total_supply - total_demand
        c += 1
    else:
        cm = np.insert(cm, [r-1], [[0], ], axis=0)
        cm[r-1][c-1] = total_demand - total_supply
        r += 1
print("\nBalanced Cost Matrix:\n")
print(cm)
i = 0
j = 0
A = np.zeros([r - 1, c - 1], dtype=int)
# IBFS Calculation
while (i < r-1) and (j < c-1):
    x = min(cm[r-1, j], cm[i, c-1])
    cm[r-1, j] = cm[r-1, j] - x
    cm[i, c-1] = cm[i, c-1] - x
    total_cost = total_cost + x * cm[i, j]
    no_alloc = no_alloc + 1
    A[i][j] = x
    if cm[r-1, j] < cm[i, c-1]:
        j = j + 1
    elif cm[r-1, j] > cm[i, c-1]:
        i = i + 1
    else:
        i = i + 1
        j = j + 1
# Output
print("\nTotal Cost: ", total_cost)
print("\nNo of Allocation: ", no_alloc)
print("\nAllocation Matrix:\n")
print(A)
if (r+c-1) == no_alloc and total_demand == total_supply:
    print("\nIt is not a Degenerate Solution")
else:
    print("\nDegenerate Solution")
