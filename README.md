# CS_255_GroupProject

Final Project - Monte Carlo estimation examples (pi and irregular-shape areas)

## Description

This project implements Monte Carlo simulations to estimate π (using a circle) and to estimate areas of irregular shapes (for example, a star-shaped polygon) using random sampling. The interactive Streamlit app visualizes how random points within a square or bounding box can be used to approximate quantities by testing whether points fall inside the target shape.

## Features

- Interactive visualization of Monte Carlo simulation
- Adjustable number of sample points (100 to 50,000)
- Real-time π and area estimation with error metrics
- Convergence graph showing accuracy improvement
- Color-coded points (green = inside circle, red = outside)
 - Irregular shape (star polygon) visualization with area estimation

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Eugenefut19/CS_255_GroupProject.git
cd CS_255_GroupProject
```

### 2. Create and activate a virtual environment (recommended)

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

## How to Run

### Run the Streamlit App (Interactive Visualization)

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

### Run the Basic Monte Carlo pi estimation Python Script

```bash
python MonteCarlo_pi_estimate.py
```

Example output:
```
Monte Carlo pi estimation summary (N=10000)
Points inside circle : 7783
Points outside circle: 2217
Percent inside       : 77.83%
Estimated pi         : 3.1132
```

## Usage

1. Launch the Streamlit app using the command above
2. Use the sidebar slider to adjust the number of sample points
3. Click "Regenerate" to run a new simulation with different random points
4. Observe the visualization and convergence graph
5. Check the statistics panel for accuracy metrics

## Irregular Shapes (Star Polygon)

This project also includes an irregular-shape example: a star-shaped polygon. The same Monte Carlo approach is used — random points are sampled in the bounding box and a point-in-polygon test decides whether a point lies inside the star. The app provides:

- A visualization of sampled points (green = inside the star, red = outside)
- An estimated area for the star polygon (displayed in the Results panel)
- A reference area (approx. 1.40) used for comparison so you can see absolute and percent error
- A convergence plot showing how the area estimate evolves as you increase sample count

Use the sidebar control in the Streamlit app to switch between "Circle" and "Star Polygon". The default sidebar slider still controls the number of sample points (100–50,000). For the star polygon the app shows matching metrics to the circle view: estimated value, reference value, absolute error, and error percentage.

## How It Works

The Monte Carlo method estimates π by:

1. Generating random points within a 2×2 square (from -1 to 1 on both axes)
1. Testing if each point falls inside the target shape (for a circle: x² + y² ≤ 1; for irregular shapes: a point-in-polygon test)
2. Calculating the ratio: (points inside shape) / (total points)
3. For the circle this ratio ≈ π/4, so multiplying by 4 gives an estimate of π. For irregular shapes the ratio times the bounding-box area gives an area estimate.

As the number of sample points increases, the estimate converges (in probability) to the true value for the chosen shape.

## Requirements

- Python 3.9+
- streamlit
- matplotlib
- numpy

## Deactivating Virtual Environment

When you're done, deactivate the virtual environment:

```bash
deactivate
```
