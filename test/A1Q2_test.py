from shapely.geometry import LineString
from matplotlib import pyplot as plt
x1 = [0, 250]
y1 = [500, 0]
x2 = [150, 150]
y2 = [0, 500]
x3 = [0, 250]
y3 = [250, 250]
plt.xlabel('X - Axis')
plt.ylabel('Y - Axis')
plt.title('Plotting')
plt.plot(x2, y2, color="red")
plt.plot(x1, y1, color="black")
plt.plot(x3, y3, color="blue")
# line 1
line1 = LineString([(0, 500), (250, 0)])
# line 2
line2 = LineString([(150, 0), (150, 500)])
# line 3
line3 = LineString([(0, 250), (250, 250)])
intersection1 = line1.intersection(line2)
intersection2 = line2.intersection(line3)
intersection3 = line3.intersection(line1)
p1, q1 = intersection1.xy
p2, q2 = intersection2.xy
p3, q3 = intersection3.xy
x1 = [0, p3[0]]
y1 = [250, q3[0]]
x2 = [p3[0], p1[0]]
y2 = [q3[0], q1[0]]
plt.plot(*intersection1.xy, 'go')
plt.plot(*intersection2.xy, 'go')
plt.plot(*intersection3.xy, 'go')
plt.plot(0, 250, 'b*')
plt.plot(150, 0, 'r*')
plt.fill_between(x1, y1, color='grey')
plt.fill_between(x2, y2, color='grey')
plt.show()
print("boundary points:")
print(150.0, " , ", 0)
print(p1[0], " , ", q1[0])
print(p3[0], " , ", q3[0])
print(0, " , ", 250.0)
# for calculating maximum profit
m1 = [0, 125, 150, 150]
m2 = [250, 250, 200, 0]
total_profit = []
for i in range(4):
    total_profit.append(8*m1[i]+5*m2[i])
max_profit = max(total_profit)
print("maximum profit is ", max_profit)
ind = total_profit.index(max_profit)
a = m1[ind]
b = m2[ind]
print("at point ", a, " , ", b)
