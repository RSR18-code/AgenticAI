import matplotlib.pyplot as plt  # type: ignore

balls = [10, 20, 30, 40, 60]
runs = [20, 30, 45, 65, 77]

fig, ax = plt.subplots(facecolor="#11112b")
ax.set_facecolor("#202047")
ax.plot(
    balls,
    runs,
    color="#35f2dc",
    marker="o",
    markersize=8,
    markerfacecolor="#ffdc55",
    markeredgecolor="#fff3b0",
    linewidth=3,
    label="Data",
)
ax.set_title("Sample Plot", color="#fff3b0", fontsize=16, fontweight="bold")
ax.set_xlabel("Balls", color="#f4f0ff")
ax.set_ylabel("Runs", color="#f4f0ff")
ax.tick_params(colors="#f4f0ff")
ax.grid(color="#a477ff", linestyle=":", linewidth=0.8, alpha=0.65)
for spine in ax.spines.values():
    spine.set_color("#a477ff")
ax.legend(facecolor="#292955", edgecolor="#a477ff", labelcolor="#f4f0ff")
fig.tight_layout()
plt.show()