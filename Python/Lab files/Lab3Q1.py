from tkinter.tix import MAX
import numpy as np
MAX_INT = 2147483647


def checkForBalanced(supply, demand):
    if np.sum(supply) == np.sum(demand):
        print("This is a balanced transportation problem")
    else:
        print("This is an unbalanced transportation problem")


def printMatrix(cost, r, c):
    for i in range(r):
        for j in range(c):
            print(cost[i][j], end=" ")
        print()


def max_penalty(cost, noOfWarehouses, noOfStores):
    rowPenalty = []
    for i in range(noOfWarehouses):
        m1 = MAX_INT
        m2 = MAX_INT
        for j in range(noOfStores):
            if cost[i][j] < m1:
                m2 = m1
                m1 = cost[i][j]
            elif cost[i][j] < m2:
                m2 = cost[i][j]
        if m1 != MAX_INT and m2 != MAX_INT:
            rowPenalty.append((m2-m1, j))
        elif m1 != MAX_INT:
            rowPenalty.append((m1, j))
        else:
            rowPenalty.append((-1, j))

    colPenalty = []
    for j in range(noOfStores):
        m1 = MAX_INT
        m2 = MAX_INT
        for i in range(noOfWarehouses):
            if cost[i][j] < m1:
                m2 = m1
                m1 = cost[i][j]
            elif cost[i][j] < m2:
                m2 = cost[i][j]
        if m1 != MAX_INT and m2 != MAX_INT:
            colPenalty.append((m2-m1, i))
        elif m1 != MAX_INT:
            colPenalty.append((m1, j))
        else:
            colPenalty.append((-1, i))

    return (rowPenalty, colPenalty)


def findMinInRow(r, n, cost):
    m = cost[r][0]
    ind = [r, 0]
    for i in range(n):
        if cost[r][i] < m:
            ind[1] = i
    return ind


def findMinInCol(c, n, cost):
    m = cost[0][c]
    ind = [0, c]
    for i in range(n):
        if cost[i][c] < m:
            ind[0] = i
    return ind


def vam(supply, demand, noOfWarehouses, noOfStores, cost, allocation):
    rowPenalty, colPenalty = max_penalty(cost, noOfWarehouses, noOfStores)
    maxRowPenalty = max(rowPenalty)
    maxColPenalty = max(colPenalty)
    maxPenalty = max([maxRowPenalty, maxColPenalty])
    totalCost = 0
    noOfAllocations = 0
    while maxPenalty[0] != -1:
        print("DEBUG")
        if maxPenalty == maxRowPenalty:
            minPos = findMinInRow(maxPenalty[1], noOfStores, cost)
        else:
            minPos = findMinInCol(maxPenalty[1], noOfWarehouses, cost)
        i = minPos[0]
        j = minPos[1]
        allocation[i][j] += min(supply[i], demand[j])
        supply[i] -= allocation[i][j]
        demand[j] -= allocation[i][j]
        totalCost += allocation[i][j]*cost[i][j]
        if supply[i] < demand[j]:
            j1 = 0
            while j1 < noOfStores:
                cost[i][j1] = MAX_INT
                j1 += 1
        elif supply[i] > demand[j]:
            i1 = 0
            while i1 < noOfWarehouses:
                cost[i1][j] = MAX_INT
                i1 += 1
        else:
            j1 = 0
            while j1 < noOfStores:
                cost[i][j1] = MAX_INT
                j1 += 1
            i1 = 0
            while i1 < noOfWarehouses:
                cost[i1][j] = MAX_INT
                i1 += 1
        noOfAllocations += 1
        rowPenalty, colPenalty = max_penalty(cost, noOfWarehouses, noOfStores)
        maxRowPenalty = max(rowPenalty)
        maxColPenalty = max(colPenalty)
        maxPenalty = max([maxRowPenalty, maxColPenalty])

    if noOfWarehouses+noOfStores-1 == noOfAllocations:
        print("\nnon-degeneracy condition is satisfied")
    else:
        print("\ndegeneracy condition is satisfied")
    return totalCost


if __name__ == "__main__":
    noOfWarehouses = 4
    noOfStores = 6
    supply = np.array([5, 6, 2, 9])
    demand = np.array([4, 4, 6, 2, 4, 2])
    cost = np.array([[9, 12, 9, 6, 9, 10],
                     [7, 3, 7, 7, 5, 5],
                     [6, 5, 9, 11, 3, 11],
                     [6, 8, 11, 2, 2, 10]])
    allocation = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
    checkForBalanced(supply, demand)
    print("Supply array:", supply)
    print("Demand array:", demand)
    print("\nCost Matrix:")
    printMatrix(cost, noOfWarehouses, noOfStores)
    totalCost = vam(supply, demand, noOfWarehouses, noOfStores, cost, allocation)
    print("\nAllocation Matrix")
    printMatrix(allocation, noOfWarehouses, noOfStores)
    print("\nTotal cost incurred:", totalCost)
