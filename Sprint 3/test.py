import matplotlib.pyplot as plt

plt.plot([0, 0, 6, 6], [0, 20, 20, 0], 'ro')
plt.plot(3,7, marker="v", color="green")
plt.axis([-1, 7, -1, 21])
plt.savefig('static/map.jpg')
plt.show()