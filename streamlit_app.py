import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from MonteCarlo_pi_estimate import estimate_pi

# Set page configuration
st.set_page_config(page_title="Monte Carlo Pi Estimator", layout="wide")

# Title and description
st.title("Monte Carlo Pi Estimation")
st.markdown("""
This app visualizes the Monte Carlo method for estimating π (pi).
Random points are thrown into a square, and we count how many fall inside the inscribed circle.

**Formula**: π ≈ 4 × (points inside circle) / (total points)
""")

# Sidebar controls
st.sidebar.header("Parameters")
n_points = st.sidebar.slider(
    "Number of Points",
    min_value=100,
    max_value=50000,
    value=5000,
    step=100,
    help="More points give a more accurate estimate"
)

point_size = st.sidebar.slider(
    "Point Size",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1
)

# Add a button to regenerate
if st.sidebar.button("Regenerate", type="primary"):
    st.rerun()

# Monte Carlo simulation wrapper with Streamlit progress bar
def monte_carlo_pi(N):
    # Use a progress bar for large simulations
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def progress_callback(current, total):
        progress_bar.progress(current / total)
        status_text.text(f"Simulating... {current}/{total} points")
    
    # Call the estimate_pi function from MonteCarlo_pi_estimate.py
    result = estimate_pi(
        N=N, 
        visualize=False, 
        track_convergence=True,
        progress_callback=progress_callback
    )
    
    progress_bar.progress(1.0)
    status_text.text(f"Simulation complete! {N} points generated.")
    
    return result

# Run simulation
pi_estimate, xs_inside, ys_inside, xs_outside, ys_outside, inside_count, convergence_points, convergence_estimates = monte_carlo_pi(n_points)

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualization")
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw square boundary
    square_x = [-1, 1, 1, -1, -1]
    square_y = [-1, -1, 1, 1, -1]
    ax.plot(square_x, square_y, 'k-', linewidth=2, label='Square')
    
    # Draw circle boundary
    circle = plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2, label='Circle')
    ax.add_patch(circle)
    
    # Scatter points
    ax.scatter(xs_inside, ys_inside, s=point_size, c='green', alpha=0.6, label=f'Inside ({inside_count})')
    ax.scatter(xs_outside, ys_outside, s=point_size, c='red', alpha=0.6, label=f'Outside ({n_points - inside_count})')
    
    ax.set_aspect('equal', 'box')
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title(f"Monte Carlo Simulation with {n_points:,} Points", fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

with col2:
    st.subheader("Results")
    
    # Display metrics
    st.metric(
        label="Estimated π",
        value=f"{pi_estimate:.6f}",
        delta=f"{pi_estimate - np.pi:.6f}"
    )
    
    st.metric(
        label="Actual π",
        value=f"{np.pi:.6f}"
    )
    
    error = abs(pi_estimate - np.pi)
    error_percentage = (error / np.pi) * 100
    
    st.metric(
        label="Absolute Error",
        value=f"{error:.6f}"
    )
    
    st.metric(
        label="Error Percentage",
        value=f"{error_percentage:.4f}%"
    )
    
    # Additional statistics
    st.subheader("Statistics")
    st.write(f"**Total Points:** {n_points:,}")
    st.write(f"**Points Inside Circle:** {inside_count:,}")
    st.write(f"**Points Outside Circle:** {n_points - inside_count:,}")
    st.write(f"**Ratio (Inside/Total):** {inside_count/n_points:.6f}")
    st.write(f"**π Estimate:** 4 × {inside_count/n_points:.6f} = {pi_estimate:.6f}")

# Add convergence graph
st.markdown("---")
st.subheader("📈 Convergence to π")
st.markdown("This graph shows how the estimate improves as more points are added:")

fig_convergence, ax_convergence = plt.subplots(figsize=(12, 6))

# Plot the convergence
ax_convergence.plot(convergence_points, convergence_estimates, 'b-', linewidth=2, label='Estimated π', alpha=0.7)

# Plot the actual value of pi
ax_convergence.axhline(y=np.pi, color='r', linestyle='--', linewidth=2, label=f'Actual π = {np.pi:.6f}')

# Add error bands
error_margin = 0.1
ax_convergence.fill_between(convergence_points, np.pi - error_margin, np.pi + error_margin, 
                             color='red', alpha=0.1, label=f'±{error_margin} error band')

ax_convergence.set_xlabel('Number of Points', fontsize=12)
ax_convergence.set_ylabel('Estimated Value of π', fontsize=12)
ax_convergence.set_title('Monte Carlo Convergence: Estimate of π vs Number of Points', fontsize=14, fontweight='bold')
ax_convergence.grid(True, alpha=0.3)
ax_convergence.legend(loc='best')
ax_convergence.set_xscale('log')  # Log scale for better visualization

# Set y-axis limits for better view
y_min = min(min(convergence_estimates), np.pi) - 0.2
y_max = max(max(convergence_estimates), np.pi) + 0.2
ax_convergence.set_ylim(y_min, y_max)

st.pyplot(fig_convergence)

# Add some statistics about convergence
col_conv1, col_conv2, col_conv3 = st.columns(3)
with col_conv1:
    initial_error = abs(convergence_estimates[0] - np.pi)
    st.metric("Initial Error (10 points)", f"{initial_error:.4f}")
with col_conv2:
    midpoint = len(convergence_estimates) // 2
    mid_error = abs(convergence_estimates[midpoint] - np.pi)
    st.metric(f"Mid Error ({convergence_points[midpoint]} points)", f"{mid_error:.4f}")
with col_conv3:
    final_error = abs(convergence_estimates[-1] - np.pi)
    st.metric(f"Final Error ({convergence_points[-1]} points)", f"{final_error:.4f}")

# Add explanation at the bottom
st.markdown("---")
st.subheader("How it works")
st.markdown("""
1. **Random Point Generation**: We generate random points within a 2×2 square (from -1 to 1 on both axes)
2. **Circle Test**: We check if each point falls inside the unit circle (radius = 1) using the formula: x² + y² ≤ 1
3. **Ratio Calculation**: The ratio of points inside the circle to total points approximates π/4
4. **Pi Estimation**: Multiply the ratio by 4 to get the estimate of π

The more points we use, the more accurate our estimate becomes! The convergence graph above shows how the estimate gets closer to the actual value of π as we add more points. Notice how the error decreases as the sample size increases.
""")
