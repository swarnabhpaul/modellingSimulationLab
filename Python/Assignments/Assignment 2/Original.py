from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
import math

# To Print Tables In A Proper Format


def dis(tn):
    t = PrettyTable()
    t.field_names = [' ', 'D1', 'D2', 'D3', 'D4', 'Sup']
    for i in range(3):
        l = []
        l.append('S' + str(i+1))
        for j in range(4):
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
    i = 1
    # Checks If We Are Within The Limits Of Table
    # Makes Allotments According To Specified Rules
    while r < 3 and c < 4:
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
        dis('Table ' + str(i))
        i += 1

# Least Cost Method


def lcm():
    print('LCM: ')
    l = []
    # Adds All Cost To A List
    for i in range(3):
        for j in range(4):
            l.append(cost[i][j])
    i = 1
    # Finds Lowest Cost
    # Allocates Value If Possible
    while max(sup) != 0:
        r = l.index(min(l))
        l[r] = infinity
        c = r % 4
        r = r // 4
        if sup[r] == 0 or dem[c] == 0:
            continue
        elif sup[r] < dem[c]:
            dem[c] -= sup[r]
            mat[r][c] = sup[r]
            sup[r] = 0
        else:
            sup[r] -= dem[c]
            mat[r][c] = dem[c]
            dem[c] = 0
        dis('Table ' + str(i))
        i += 1


# Giving Input, & Defining Variables
infinity = math.inf
mat = [[0 for i in range(4)] for i in range(3)]
cost = [[21, 16, 15, 3],
        [17, 18, 14, 23],
        [32, 27, 18, 41]]
sup = [11, 13, 19]
dem = [6, 10, 12, 15]
nwcr()
print()
print()
mat = [[0 for i in range(4)] for i in range(3)]
sup = [11, 13, 19]
dem = [6, 10, 12, 15]
lcm()
