from matplotlib import pyplot as plt
from shapely.geometry import LineString
line1 = LineString([(0,6),(12,0)])
line2 = LineString([(0,10),(10,0)])
plt.plot(*line1.xy)
plt.plot(*line2.xy)
intersection = line1.intersection(line2)
plt.plot(*intersection.xy,"ro")
plt.show()