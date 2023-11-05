import numpy as np
import matplotlib.pyplot as plt

# Parameters
width, height = 600, 600
point_count = 20
grid_count = 20
gravity_force = 2000
falloff = 2

# Random points simulating gravitational mass
points = np.random.rand(point_count, 2) * [width, height]

# Calculate grid points affected by the 'gravitational' points
def do_calculation():
    grid = []
    for yi in range(grid_count):
        row = []
        for xi in range(grid_count):
            x = (width / grid_count) * xi # Normal coordinates
            y = (height / grid_count) * yi # Normal coordinates

            for px, py in points:
                dx = px - x
                dy = py - y
                d = np.sqrt(dx**2 + dy**2)
                if d > 0:
                    a = np.arctan2(dy, dx)
                    f = gravity_force / np.power(d, falloff)
                    f = f if f < d else d
                    x += np.cos(a) * f
                    y += np.sin(a) * f

            row.append([x, y])
        grid.append(row)
    return np.array(grid)

grid = do_calculation()

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Draw the grid lines
for yi in range(grid_count):
    ax.plot(grid[yi, :, 0], grid[yi, :, 1], color='black', lw=1)
    ax.plot(grid[:, yi, 0], grid[:, yi, 1], color='black', lw=1)

# Draw the 'gravitational' points
for point in points:
    ax.scatter(*point, color='purple', s=50)

# Set the plot limits and aspect
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')
ax.axis('off')

plt.show()