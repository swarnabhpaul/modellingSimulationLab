from shapely.geometry import LineString
from matplotlib import pyplot as plt
# line 1
x1 = [2, 0]
y1 = [0, 10]
plt.plot(x1, y1, color="red")
# line 2
x2 = [6, 0]
y2 = [0, 6]
plt.plot(x2, y2, color="green")
# line 3
x3 = [12, 0]
y3 = [0, 3]
plt.plot(x3, y3, color="black")
plt.xlabel('X - Axis')
plt.ylabel('Y - Axis')
plt.title('Plotting')
line1 = LineString([(2, 0), (0, 10)])
line2 = LineString([(6, 0), (0, 6)])
line3 = LineString([(12, 0), (0, 3)])
intersection1 = line2.intersection(line3)
intersection2 = line1.intersection(line2)
intersection3 = line3.intersection(line1)
plt.plot(0, 10, 'b*')
plt.plot(12, 0, 'r*')
p1, q1 = intersection1.xy
p2, q2 = intersection2.xy
p3, q3 = intersection3.xy
plt.plot(*intersection1.xy, 'go')
plt.plot(*intersection2.xy, 'go')
plt.plot(*intersection3.xy, 'go')
x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
x1.append(0)
x1.append(p2[0])
y1.append(10)
y1.append(q2[0])
x2.append(p2[0])
x2.append(p1[0])
y2.append(q2[0])
y2.append(q1[0])
x3.append(p1[0])
x3.append(12)
y3.append(q1[0])
y3.append(0)
print("x1, y1: ", x1, y1)
print("x2, y2: ", x2, y2)
print("x3, y3: ", x3, y3)
plt.fill_between(x1, y1, 10, color='blue')
plt.fill_between(x2, y2, 10, color='blue')
plt.fill_between(x3, y3, 10, color='blue')
plt.show()
print("Boundary points are")
print(0, 10.0)
print(p1[0], q1[0])
print(p2[0], q2[0])
print(12.0, 0)
cost = []
m1 = [0, p1[0], p2[0], 12]
m2 = [10.0, q1[0], q2[0], 0]
for i in range(4):
    cost.append(3*m1[i]+2*m2[i])
min_cost = min(cost)
print("minimum cost --> ", min_cost)
ind = cost.index(min_cost)
a = m1[ind]
b = m2[ind]
print("at point ", a, " , ", b)
