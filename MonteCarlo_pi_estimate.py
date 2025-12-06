import random
import matplotlib.pyplot as plt

# Monte Carlo estimation of pi with visualization

def estimate_pi(N=100, progress_callback=None):
    """
    Monte Carlo estimation of pi.
    
    Args:
        N: Number of random points to generate
        progress_callback: Optional callback function for progress updates (used by Streamlit)
    
    Returns:
        (pi_estimate, xs_inside, ys_inside, xs_outside, 
        ys_outside, inside_count, convergence_points, convergence_estimates)
    """
    inside_count = 0
    xs_inside = []
    ys_inside = []
    xs_outside = []
    ys_outside = []
    
    # Track estimates at different intervals for convergence plot
    convergence_points = []
    convergence_estimates = []
    
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
            inside_count += 1
            xs_inside.append(x)
            ys_inside.append(y)
        else:
            xs_outside.append(x)
            ys_outside.append(y)
        
        if (i + 1) in sample_intervals:
            pi_est = 4 * inside_count / (i + 1)
            convergence_points.append(i + 1)
            convergence_estimates.append(pi_est)
        
        # Call progress callback if provided
        if progress_callback and i % 1000 == 0:
            progress_callback(i + 1, N)

    pi_estimate = 4 * inside_count / N

    return pi_estimate, xs_inside, ys_inside, xs_outside, ys_outside, inside_count, convergence_points, convergence_estimates

if __name__ == "__main__":
    N = 10000
    result = estimate_pi(N)
    pi_estimate, xs_inside, ys_inside, xs_outside, ys_outside, inside_count, convergence_points, convergence_estimates = result
    outside_count = N - inside_count

    print(f"Monte Carlo pi estimation summary (N={N})")
    print(f"Points inside circle : {inside_count}")
    print(f"Points outside circle: {outside_count}")
    print(f"Percent inside       : {inside_count / N * 100:.2f}%")
    print(f"Estimated pi         : {pi_estimate:.4f}")
