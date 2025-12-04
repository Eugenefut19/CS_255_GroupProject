import random
import matplotlib.pyplot as plt

# Monte Carlo estimation of pi with visualization

def estimate_pi(N=100, visualize=True, track_convergence=False, progress_callback=None):
    """
    Monte Carlo estimation of pi.
    
    Args:
        N: Number of random points to generate
        visualize: If True, shows a matplotlib visualization
        track_convergence: If True, tracks estimates at intervals for convergence analysis
        progress_callback: Optional callback function for progress updates (used by Streamlit)
    
    Returns:
        If track_convergence is False: pi_estimate
        If track_convergence is True: (pi_estimate, xs_inside, ys_inside, xs_outside, 
                                        ys_outside, inside_count, convergence_points, convergence_estimates)
    """
    inside = 0
    xs_inside = []
    ys_inside = []
    xs_outside = []
    ys_outside = []
    
    # Track estimates at different intervals for convergence plot
    convergence_points = []
    convergence_estimates = []
    
    if track_convergence:
        # Sample at logarithmic intervals for better visualization
        sample_intervals = set()
        for i in range(10, N+1):
            if i in [10, 50, 100, 250, 500, 750, 1000]:
                sample_intervals.add(i)
            elif i % max(1, N // 100) == 0:  # Sample ~100 points
                sample_intervals.add(i)
        sample_intervals.add(N)  # Always include the final point

    for i in range(N):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
            xs_inside.append(x)
            ys_inside.append(y)
        else:
            xs_outside.append(x)
            ys_outside.append(y)
        
        # Track convergence if requested
        if track_convergence and (i + 1) in sample_intervals:
            pi_est = 4 * inside / (i + 1)
            convergence_points.append(i + 1)
            convergence_estimates.append(pi_est)
        
        # Call progress callback if provided
        if progress_callback and i % 1000 == 0:
            progress_callback(i + 1, N)

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

    if track_convergence:
        return pi_estimate, xs_inside, ys_inside, xs_outside, ys_outside, inside, convergence_points, convergence_estimates
    else:
        return pi_estimate

if __name__ == "__main__":
    print("Estimated pi:", estimate_pi(10000, visualize=True))
