import numpy as np
import os
import sys

"""4 6
5 6 2 9
4 4 6 2 4 2
9 12 9 6 9 10
7 3 7 7 5 5
6 5 9 11 3 11
6 8 11 2 2 10"""

sys.stdin = open('in.txt', 'r')


def In():
    return list(map(int, sys.stdin.readline().split()))


p, d = In()
sup = np.array(In())
dem = np.array(In())
mat = np.array([np.array(In()) for _ in range(p)])
mat = mat.astype('float64')


def check_balanced(supply, demand):
    return np.sum(supply) == np.sum(demand)


def check_degeneracy(mat, alloc):
    return np.sum(mat.shape)-1 == alloc


if check_balanced(sup, dem):
    print("Question is balanced.")
else:
    print("Question not balanced. Applying modifications.")
    sup_sum = sum(sup)
    dem_sum = sum(dem)
    if sup_sum < dem_sum:
        mat = np.append(mat, np.array(np.zeros((1, d))), axis=0)
        sup = np.append(sup, dem_sum-sup_sum)
        p += 1
    elif sup_sum > dem_sum:
        mat = np.concatenate((mat, np.zeros((p, 1))), axis=1)
        dem = np.append(dem, sup_sum-dem_sum)
        d += 1


def get_min_min2(arr):
    m1 = m2 = np.inf
    idx1 = idx2 = -1
    for i in range(len(arr)):
        if arr[i] < m1:
            m1, m2 = arr[i], m1
        elif arr[i] < m2:
            m2 = arr[i]
    return m1, m2


def get_max_penalty(cm):
    def get_penalty(arr):
        m1, m2 = get_min_min2(arr)
        if np.inf not in (m1, m2):
            return (m2-m1)
        elif m1 != np.inf:
            return m1
    row_pen = []
    for i in range(cm.shape[0]):
        _x = get_penalty(cm[i, :])
        if _x is not None:
            row_pen.append((_x, i))

    col_pen = []
    for i in range(cm.shape[1]):
        _x = get_penalty(cm[:, i])
        if _x is not None:
            col_pen.append((_x, i))
    # print('row_pen',row_pen)
    # print('col_pen', col_pen)
    if not (col_pen or row_pen):
        return -1, -1, None
    r_mx, c_mx = max(row_pen), max(col_pen)
    if r_mx > c_mx:
        mx, i = r_mx
        mn_idx = (i, np.argmin(cm[i, :]))
        mn = cm[mn_idx]
    else:
        mx, j = c_mx
        mn_idx = np.argmin(cm[:, j]), j
        mn = cm[mn_idx]
    return mn_idx+(mn,)


i, j, mp = get_max_penalty(mat)
ans = tot_alloc = 0
temp = np.zeros((p, d))

while mp is not None:
    print("selected for alloc: ({}, {})".format(i, j))
    x = min(sup[i], dem[j])
    sup[i] -= x
    dem[j] -= x
    ans += x*mat[i, j]
    tot_alloc += 1
    temp[i, j] = x
    if sup[i] <= dem[j]:
        mat[i, :] = np.inf

    if sup[i] >= dem[j]:
        mat[:, j] = np.inf
    i, j, mp = get_max_penalty(mat)

print(ans)

print(temp)
