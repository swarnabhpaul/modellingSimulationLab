import numpy as np


def checkForBalanced(supply, demand):
    if np.sum(supply) == np.sum(demand):
        print("This is a balanced transportation problem")
    else:
        print("This is an unbalanced transportation problem")


def nwcr(supply, demand, noOfPlants, noOfCenters, cost, allocation):
    totalCost = 0
    i = 0
    j = 0
    while i < noOfPlants or j < noOfCenters:
        if supply[i] > demand[j]:
            allocation[i][j] = demand[j]
            supply[i] -= allocation[i][j]
            demand[j] -= allocation[i][j]
            totalCost += cost[i][j]*allocation[i][j]
            j += 1
        elif supply[i] < demand[j]:
            allocation[i][j] = supply[i]
            supply[i] -= allocation[i][j]
            demand[j] -= allocation[i][j]
            totalCost += cost[i][j]*allocation[i][j]
            i += 1
        else:
            allocation[i][j] = demand[j]
            supply[i] -= allocation[i][j]
            demand[j] -= allocation[i][j]
            totalCost += cost[i][j]*allocation[i][j]
            j += 1
            i += 1
    return totalCost


def printMatrix(cost, r, c):
    for i in range(r):
        for j in range(c):
            print(cost[i][j], end=" ")
        print()


if __name__ == "__main__":
    noOfPlants = 3
    noOfCenters = 4
    supply = np.array([6, 1, 10])
    demand = np.array([7, 5, 3, 2])
    cost = np.array([[2, 3, 11, 7],
                     [1, 0, 6, 1],
                     [5, 8, 15, 9]])
    allocation = np.array([[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]])
    checkForBalanced(supply, demand)
    print("Supply array:", supply)
    print("Demand array:", demand)
    print("\nCost Matrix:")
    printMatrix(cost, noOfPlants, noOfCenters)
    totalCost = nwcr(supply, demand, noOfPlants, noOfCenters, cost, allocation)
    print("\nAllocation Matrix")
    printMatrix(allocation, noOfPlants, noOfCenters)
    print("\nTotal cost incurred:", totalCost)
