# convex_hull.py
import matplotlib.pyplot as plt
import numpy as np

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Colinear
    elif val > 0:
        return 1  # Clockwise
    else:
        return 2  # Counterclockwise

def gift_wrapping_algorithm(points):
    n = len(points)
    if n < 3:
        return None

    hull = []
    l = min(points)
    p = points.index(l)

    hull.append(p)
    q = None
    while True:
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == hull[0]:
            break
        hull.append(p)

    return [points[i] for i in hull]

def graham_scan(points):
    def polar_angle(p0, p1):
        return np.arctan2(p1[1] - p0[1], p1[0] - p0[0])

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    if len(points) < 3:
        return None

    start_point = min(points, key=lambda x: (x[1], x[0]))
    sorted_points = sorted(points, key=lambda x: (polar_angle(start_point, x), -x[1], x[0]))

    stack = [sorted_points[0], sorted_points[1], sorted_points[2]]

    for i in range(3, len(sorted_points)):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], sorted_points[i]) != 2:
            stack.pop()
        stack.append(sorted_points[i])

    return stack

def divide_and_conquer(points):
    def merge(hull1, hull2):
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        def keep_left(hull, r):
            while len(hull) > 1 and cross_product(hull[-2], hull[-1], r) < 0:
                hull.pop()
            if not hull or hull[-1] != r:
                hull.append(r)
            return hull

        hull = keep_left(hull1[:], hull2[0])
        hull.extend(keep_left(hull2[:], hull1[-1]))
        return hull

    def divide(points):
        if len(points) <= 5:
            return gift_wrapping_algorithm(points)

        mid = len(points) // 2
        left_hull = divide(points[:mid])
        right_hull = divide(points[mid:])
        return merge(left_hull, right_hull)

    if len(points) < 3:
        return None

    points = sorted(set(points))
    if len(points) <= 3:
        return points

    return divide(points)

def plot_convex_hull(points, hull, algorithm):
    plt.figure(figsize=(8, 6))

    # Plot points
    plt.scatter([point[0] for point in points], [point[1] for point in points], color='blue', label='Points')

    # Plot convex hull
    for i in range(len(hull)):
        plt.plot([hull[i][0], hull[(i + 1) % len(hull)][0]],
                 [hull[i][1], hull[(i + 1) % len(hull)][1]],
                 color='red', linestyle='-', linewidth=2)

    plt.title(f'Convex Hull Visualization ({algorithm})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()

    # Save plot as base64 encoded string
    import io
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = buffer.getvalue()
    buffer.close()

    import base64
    plot_encoded = base64.b64encode(plot_data).decode('utf-8')

    return plot_encoded
