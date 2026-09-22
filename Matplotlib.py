import matplotlib.pyplot as plt  # type: ignore

balls = [10, 20, 30, 40, 50]
runs = [20, 30, 45, 65, 77]

plt.plot(balls, runs)
plt.title("Sample Plot")
plt.xlabel("Balls")
plt.ylabel("Runs")
plt.legend(["Data"])
plt.show()