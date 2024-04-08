import matplotlib.pyplot as plt
import numpy as np


def draw_line(points):
    def slope(x1, y1, x2, y2):
        return (y2 - y1) / (x2 - x1)

    # Calculate the slope for each segment between points
    slopes = [slope(x1, y1, x2, y2) for (x1, y1), (x2, y2) in zip(points[:-1], points[1:])]

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot the points
    x_vals, y_vals = zip(*points)
    ax.plot(x_vals, y_vals, marker='o')

    # Annotate each point with its slope
    for i, ((x1, y1), (x2, y2), m) in enumerate(zip(points[:-1], points[1:], slopes)):
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2  # Midpoint for annotation
        ax.annotate(f'{m:.2f}', (mid_x, mid_y), textcoords="offset points", xytext=(0, 5), ha='center')

    # Add axis labels
    ax.set_xlabel('anchor_num')
    ax.set_ylabel('fitness')

    # Show the plot
    plt.show()


data = [(2, 20657.96639), (3, 11527.68756), (4, 65781.84199), (5, 86111.53585),
           (6, 345744.34998), (7, 0.82070), (8, 0.83983), (9, 0.84685),
           (10, 0.84762)]
data = [(d[0], 1-d[1]) for d in data]

draw_line(data)
