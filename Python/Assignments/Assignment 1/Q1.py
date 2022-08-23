"""
Name: Swarnabh Paul
Roll no.: 19CS8122
"""

from matplotlib import pyplot as plt
from shapely.geometry import LineString
line1 = LineString([(0, 10), (2, 0)])
line2 = LineString([(0, 6), (6, 0)])
line3 = LineString([(0, 3), (12, 0)])
plt.plot(*line1.xy)
plt.plot(*line2.xy)
plt.plot(*line3.xy)
intersection1 = line1.intersection(line2)
intersection2 = line2.intersection(line3)
plt.plot(*intersection1.xy, "ro")
plt.plot(*intersection2.xy, "ro")
boundaryPts = []
boundaryPts.append((0, 10))
boundaryPts.append((12, 0))
x1, x2 = intersection1.xy
boundaryPts.append((x1[0], x2[0]))
x1, x2 = intersection2.xy
boundaryPts.append((x1[0], x2[0]))
print("Boundary points:", boundaryPts)
minCost = -1
minCostIndex = -1
for i in range(len(boundaryPts)):
    x1 = boundaryPts[i][0]
    x2 = boundaryPts[i][1]
    cost = 3*x1+2*x2
    if cost < minCost or minCost == -1:
        minCost = cost
        minCostIndex = i
print("Minimum cost:", minCost)
print("At x1 = ", boundaryPts[minCostIndex][0], ", x2 = ", boundaryPts[minCostIndex][1], sep="")
plt.xlabel("x1 ->")
plt.ylabel("x2 ->")
plt.show()
