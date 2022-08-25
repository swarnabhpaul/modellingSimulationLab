import numpy as np


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
    min_cost = np.amin(cost)
    while min_cost != np.inf:
        result = np.where()


if __name__ == "__main__":
    noOfWarehouses = 4
    noOfStores = 6
    supply = np.array([5, 6, 2, 9])
    demand = np.array([4, 4, 6, 2, 4, 2])
    cost = np.array([[9, 12, 9, 6, 9, 10],
                     [7, 3, 7, 7, 5, 5],
                     [6, 5, 9, 11, 3, 11],
                     [6, 8, 11, 2, 2, 10]])
    allocation = np.array([[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]])
    checkForBalanced(supply, demand)
    print("Supply array:", supply)
    print("Demand array:", demand)
    print("\nCost Matrix:")
    printMatrix(cost, noOfWarehouses, noOfStores)
    totalCost = lcm(supply, demand, noOfWarehouses, noOfStores, cost, allocation)
    print("\nAllocation Matrix")
    printMatrix(allocation, noOfWarehouses, noOfStores)
    print("\nTotal cost incurred:", totalCost)
