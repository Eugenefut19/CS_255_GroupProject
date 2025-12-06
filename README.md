# CS_255_GroupProject

Final Project - Estimation of pi using Monte Carlo

## Description

This project implements a Monte Carlo simulation to estimate the value of π (pi) using random sampling. The interactive Streamlit app visualizes how random points within a square can be used to approximate π based on whether they fall inside an inscribed circle.

## Features

- Interactive visualization of Monte Carlo simulation
- Adjustable number of sample points (100 to 50,000)
- Real-time π estimation with error metrics
- Convergence graph showing accuracy improvement
- Color-coded points (green = inside circle, red = outside)

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

### Run the Basic Python Script

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

## How It Works

The Monte Carlo method estimates π by:

1. Generating random points within a 2×2 square (from -1 to 1 on both axes)
2. Testing if each point falls inside the unit circle (x² + y² ≤ 1)
3. Calculating the ratio: (points inside circle) / (total points) ≈ π/4
4. Multiplying by 4 to estimate π

As the number of sample points increases, the estimate converges closer to the actual value of π.

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
