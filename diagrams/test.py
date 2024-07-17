import matplotlib.pyplot as plt

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 10))

# Define box properties
box_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgrey")

# Add boxes for each component
components = [
    ("Babel API", (0.5, 0.8)),
    ("Babel Bot", (0.8, 0.6)),
    ("Babel Data", (0.2, 0.6)),
    ("Babel Agent", (0.2, 0.4)),
    ("Babel CLI", (0.8, 0.4)),
]

for component in components:
    ax.text(
        component[1][0],
        component[1][1],
        component[0],
        transform=ax.transAxes,
        fontsize=14,
        verticalalignment="top",
        horizontalalignment="center",
        bbox=box_props,
    )

# Add arrows to show interaction
arrows = [
    ((0.5, 0.78), (0.8, 0.62)),  # API to Bot
    ((0.8, 0.58), (0.5, 0.78)),  # Bot to API
    ((0.5, 0.78), (0.2, 0.62)),  # API to Data
    ((0.2, 0.58), (0.5, 0.78)),  # Data to API
    ((0.2, 0.58), (0.2, 0.42)),  # Data to Agent
    ((0.2, 0.38), (0.2, 0.58)),  # Agent to Data
    ((0.8, 0.38), (0.5, 0.78)),  # CLI to API
    ((0.5, 0.78), (0.8, 0.38)),  # API to CLI
]

for arrow in arrows:
    ax.annotate(
        "",
        xy=arrow[1],
        xytext=arrow[0],
        xycoords="axes fraction",
        arrowprops=dict(facecolor="black", arrowstyle="->"),
    )

# Add title
plt.title("Babel Project System Architecture", fontsize=16)

# Remove axes
ax.axis("off")

# Display diagram
plt.show()
