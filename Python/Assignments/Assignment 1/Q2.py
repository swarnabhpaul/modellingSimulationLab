"""
Name: Swarnabh Paul
Roll no.: 19CS8122
"""

from matplotlib import pyplot as plt
from shapely.geometry import LineString
line1 = LineString([(0, 250), (250, 250)])
line2 = LineString([(150, 500), (150, 0)])
line3 = LineString([(0, 500), (250, 0)])
plt.plot(*line1.xy)
plt.plot(*line2.xy)
plt.plot(*line3.xy)
intersection1 = line1.intersection(line3)
intersection2 = line2.intersection(line3)
plt.plot(*intersection1.xy, "ro")
plt.plot(*intersection2.xy, "ro")
boundaryPts = []
boundaryPts.append((0, 0))
boundaryPts.append((150, 0))
boundaryPts.append((0, 250))
x1, x2 = intersection1.xy
boundaryPts.append((x1[0], x2[0]))
x1, x2 = intersection2.xy
boundaryPts.append((x1[0], x2[0]))
print("Boundary points:", boundaryPts)
maxCost = -1
maxCostIndex = -1
for i in range(len(boundaryPts)):
    x1 = boundaryPts[i][0]
    x2 = boundaryPts[i][1]
    cost = 8*x1+5*x2
    if cost > maxCost or maxCost == -1:
        maxCost = cost
        maxCostIndex = i
print("Minimum cost:", maxCost)
print("At x = ", boundaryPts[maxCostIndex][0], ", y = ", boundaryPts[maxCostIndex][1], sep="")
plt.xlabel("x ->")
plt.ylabel("y ->")
plt.show()
