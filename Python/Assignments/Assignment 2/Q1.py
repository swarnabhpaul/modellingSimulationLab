from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
import math

# To Print Tables In A Proper Format


def dis(tn):
    t = PrettyTable()
    t.field_names = [' ', 'D', 'E', 'F', 'G', 'H', 'Sup']
    for i in range(3):
        l = []
        l.append(chr(65 + i))
        for j in range(5):
            l.append(str(cost[i][j]) + '(' + str(mat[i][j]) + ')')
        l.append(sup[i])
        t.add_row(l)
    l = []
    l.append('Dem')
    for i in dem:
        l.append(str(i))
    l.append(' ')
    t.add_row(l)
    t.set_style(MSWORD_FRIENDLY)
    t.border = False
    print(tn + ': ')
    print(t)

# North-West Corner Method


def nwcr():
    print('NWCR: ')
    r = 0
    c = 0
    # Checks If We Are Within The Limits Of Table
    # Makes Allotments According To Specified Rules
    while r < 3 and c < 5:
        if sup[r] < dem[c]:
            dem[c] -= sup[r]
            mat[r][c] = sup[r]
            sup[r] = 0
            r += 1
        elif dem[c] < sup[r]:
            sup[r] -= dem[c]
            mat[r][c] = dem[c]
            dem[c] = 0
            c += 1
        else:
            mat[r][c] = sup[r]
            sup[r] = 0
            dem[c] = 0
            r += 1
            c += 1
    dis('Final Table')


# Giving Input, & Defining Variables
infinity = math.inf
mat = [[0 for i in range(5)] for i in range(3)]
cost = [[5, 8, 6, 6, 3],
        [4, 7, 7, 6, 5],
        [8, 4, 6, 6, 4]]
sup = [800, 500, 900]
dem = [400, 400, 500, 400, 800]
print("Supply vector: ", sup)
print("Demand vector: ", dem)
print("Cost matrix: ")
for i in range(3):
    for j in range(5):
        print(cost[i][j], end=" ")
    print()
print()
nwcr()
print()
total = 0
for i in range(3):
    for j in range(5):
        total += mat[i][j] * cost[i][j]
print("Total cost:", total)
