import random
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


class streamlitStar:
    def __init__(self, n_points, point_size):
        self.n_points = n_points
        self.point_size = point_size
        self.star_vertices = [
            (0.0, 1.0),
            (0.35, 0.35),
            (1.0, 0.0),
            (0.35, -0.35),
            (0.0, -1.0),
            (-0.35, -0.35),
            (-1.0, 0.0),
            (-0.35, 0.35),
        ]

        (
            self.area_estimate,
            self.xs_inside,
            self.ys_inside,
            self.xs_outside,
            self.ys_outside,
            self.inside_count,
            self.convergence_points,
            self.convergence_estimates,
        ) = self.monte_carlo_star()

    def visualize(self):
        self.visualize_monte_carlo()
        self.visualize_convergence_graph()
        self.visualize_explanation()

    def visualize_explanation(self):
        st.markdown("---")
        st.subheader("How it works")
        st.markdown("""
        1. We generate random points inside the bounding box around the star.
        2. We test each point with a point-in-polygon (ray-casting) test to see if it's inside the star.
        3. The fraction of points inside multiplied by the bounding box area gives the star's estimated area.
        """)

    def visualize_convergence_graph(self):
        st.markdown("---")
        st.subheader("📈 Convergence of Area Estimate")
        st.markdown("This graph shows the estimated area at sampled intervals as the number of points increases:")

        fig_convergence, ax_convergence = plt.subplots(figsize=(12, 6))

        ax_convergence.plot(self.convergence_points, self.convergence_estimates, 'b-', linewidth=2, label='Estimated Area', alpha=0.7)

        final_est = self.convergence_estimates[-1]
        ax_convergence.axhline(y=final_est, color='r', linestyle='--', linewidth=2, label=f'Final estimate = {final_est:.6f}')

        k = min(10, max(1, len(self.convergence_estimates) // 10))
        recent = np.array(self.convergence_estimates[-k:])
        std_recent = float(np.std(recent)) if recent.size > 1 else 0.0
        rel_margin = 0.05 * abs(final_est) if final_est != 0 else 0.05
        margin = max(std_recent, 0.2 * rel_margin)
        ax_convergence.fill_between(self.convergence_points, np.array(self.convergence_estimates) - margin, np.array(self.convergence_estimates) + margin,
                                     color='red', alpha=0.1, label=f'±{margin:.4f} error band')

        ax_convergence.set_xlabel('Number of Points', fontsize=12)
        ax_convergence.set_ylabel('Estimated Area', fontsize=12)
        ax_convergence.set_title('Monte Carlo Convergence: Estimated Area vs Number of Points', fontsize=14, fontweight='bold')
        ax_convergence.grid(True, alpha=0.3)
        ax_convergence.legend(loc='best')
        ax_convergence.set_xscale('log')

        y_min = min(min(self.convergence_estimates), final_est) - margin * 2
        y_max = max(max(self.convergence_estimates), final_est) + margin * 2
        ax_convergence.set_ylim(y_min, y_max)

        st.pyplot(fig_convergence)

        col_conv1, col_conv2, col_conv3 = st.columns(3)
        with col_conv1:
            initial_error = abs(self.convergence_estimates[0] - final_est)
            st.metric("Initial Error (sample)", f"{initial_error:.4f}")
        with col_conv2:
            midpoint = len(self.convergence_estimates) // 2
            mid_error = abs(self.convergence_estimates[midpoint] - final_est)
            st.metric(f"Mid Error ({self.convergence_points[midpoint]} points)", f"{mid_error:.4f}")
        with col_conv3:
            final_error = abs(self.convergence_estimates[-1] - final_est)
            st.metric(f"Final Error ({self.convergence_points[-1]} points)", f"{final_error:.4f}")

    def visualize_monte_carlo(self):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Visualization")

            fig_convergence, ax_convergence = plt.subplots(figsize=(8, 8))

            # outline polygon
            vx, vy = zip(*(self.star_vertices + [self.star_vertices[0]]))
            ax_convergence.plot(vx, vy, color='black', linewidth=2)

            # scatter points
            ax_convergence.scatter(self.xs_inside, self.ys_inside, s=self.point_size, c='green', alpha=0.6, label=f'Inside ({self.inside_count})')
            ax_convergence.scatter(self.xs_outside, self.ys_outside, s=self.point_size, c='red', alpha=0.6, label=f'Outside ({self.n_points - self.inside_count})')

            ax_convergence.set_aspect('equal', 'box')
            ax_convergence.set_xlim(-1.1, 1.1)
            ax_convergence.set_ylim(-1.1, 1.1)
            ax_convergence.set_xlabel('X', fontsize=12)
            ax_convergence.set_ylabel('Y', fontsize=12)
            ax_convergence.set_title(f"Monte Carlo Sampling on Star Polygon ({self.n_points:,} points)", fontsize=14, fontweight='bold')
            ax_convergence.legend(loc='upper right')
            ax_convergence.grid(True, alpha=0.3)

            st.pyplot(fig_convergence)

        with col2:
            st.subheader("Results")
            box_area = 4.0
            known_area = 1.40

            abs_error = abs(self.area_estimate - known_area)
            error_percentage = (abs_error / known_area) * 100 if known_area != 0 else 0.0

            st.metric(label="Estimated Area", value=f"{self.area_estimate:.6f}",
                      delta=f"{self.area_estimate - known_area:.6f}")
            st.metric(label="Reference Area (approx.)", value=f"{known_area:.6f}")

            st.metric(
                label="Absolute Error",
                value=f"{abs_error:.6f}"
            )

            st.metric(
                label="Error Percentage",
                value=f"{error_percentage:.4f}%"
            )

            st.subheader("Statistics")
            st.write(f"**Total Points:** {self.n_points:,}")
            st.write(f"**Points Inside Star:** {self.inside_count:,}")
            st.write(f"**Points Outside Star:** {self.n_points - self.inside_count:,}")
            st.write(f"**Ratio (Inside/Total):** {self.inside_count/self.n_points:.6f}")
            st.write(f"**Area Estimate Calculation:** {self.inside_count}/{self.n_points} × {box_area} = {self.area_estimate:.6f}")

    def monte_carlo_star(self):
        progress_bar = st.progress(0)
        status_text = st.empty()

        xs_inside = []
        ys_inside = []
        xs_outside = []
        ys_outside = []
        inside_count = 0

        N = self.n_points
        convergence_points = []
        convergence_estimates = []
        sample_intervals = set()
        for i in range(10, N+1):
            if i in [10, 50, 100, 250, 500, 750, 1000]:
                sample_intervals.add(i)
            elif i % max(1, N // 100) == 0:
                sample_intervals.add(i)
        sample_intervals.add(N)

        xmin, xmax = -1, 1
        ymin, ymax = -1, 1
        box_area = (xmax - xmin) * (ymax - ymin)

        def progress_callback(current, total):
            progress_bar.progress(current / total)
            status_text.text(f"Simulating... {current}/{total} points")

        for i in range(N):
            x = random.uniform(xmin, xmax)
            y = random.uniform(ymin, ymax)

            if self.inside_polygon(x, y):
                inside_count += 1
                xs_inside.append(x)
                ys_inside.append(y)
            else:
                xs_outside.append(x)
                ys_outside.append(y)

            if (i + 1) in sample_intervals:
                est = box_area * inside_count / (i + 1)
                convergence_points.append(i + 1)
                convergence_estimates.append(est)

            # update progress occasionally
            if i % max(1, N // 100) == 0:
                progress_callback(i + 1, N)

        progress_bar.progress(1.0)
        status_text.text(f"Simulation complete! {N} points generated.")

        area_estimate = box_area * inside_count / N if N > 0 else 0.0

        return (
            area_estimate,
            xs_inside,
            ys_inside,
            xs_outside,
            ys_outside,
            inside_count,
            convergence_points,
            convergence_estimates,
        )

    def inside_polygon(self, x, y):
        inside = False
        n = len(self.star_vertices)

        for i in range(n):
            x1, y1 = self.star_vertices[i]
            x2, y2 = self.star_vertices[(i + 1) % n]

            intersect = ((y1 > y) != (y2 > y)) and \
                        (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)

            if intersect:
                inside = not inside

        return inside


