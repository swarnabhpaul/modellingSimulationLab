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


def lcm(supply, demand, noOfWarehouses, noOfStores, cost, allocation):
    minCost = np.amin(cost)
    totalCost = 0
    noOfAllocations = 0
    while minCost != MAX_INT:
        result = np.where(cost == minCost)
        indexes = list(zip(result[0], result[1]))
        maxallind = 0
        maxalloc = 0
        ind = 0
        for i, j in indexes:
            if min(supply[i], demand[j]) > maxalloc:
                maxalloc = min(supply[i], demand[j])
                maxallind = ind
            ind += 1
        i = indexes[maxallind][0]
        j = indexes[maxallind][1]
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
        minCost = np.amin(cost)

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
    totalCost = lcm(supply, demand, noOfWarehouses, noOfStores, cost, allocation)
    print("\nAllocation Matrix")
    printMatrix(allocation, noOfWarehouses, noOfStores)
    print("\nTotal cost incurred:", totalCost)
