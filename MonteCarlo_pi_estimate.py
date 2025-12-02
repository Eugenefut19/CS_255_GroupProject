import random
import matplotlib.pyplot as plt

# Monte Carlo estimation of pi with visualization

def estimate_pi(N=100, visualize=True):
    inside = 0
    xs_inside = []
    ys_inside = []
    xs_outside = []
    ys_outside = []

    for _ in range(N):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
            xs_inside.append(x)
            ys_inside.append(y)
        else:
            xs_outside.append(x)
            ys_outside.append(y)

    pi_estimate = 4 * inside / N

    if visualize:
        fig, ax = plt.subplots(figsize=(6, 6))

        # Draw square boundary
        square_x = [-1, 1, 1, -1, -1]
        square_y = [-1, -1, 1, 1, -1]
        ax.plot(square_x, square_y)

        # Draw circle boundary
        circle = plt.Circle((0, 0), 1, color='black', fill=False)
        ax.add_patch(circle)

        # Scatter points
        ax.scatter(xs_inside, ys_inside, s=1)
        ax.scatter(xs_outside, ys_outside, s=1)

        ax.set_aspect('equal', 'box')
        ax.set_title(f"Monte Carlo Pi Estimate: {pi_estimate}")

        plt.show()

    return pi_estimate

if __name__ == "__main__":
    print("Estimated pi:", estimate_pi(10000, visualize=True))
