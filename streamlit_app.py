import streamlit as st
from streamlit_circle import streamlitCircle
from streamlit_star import streamlitStar

st.set_page_config(page_title="Monte Carlo Estimator", layout="wide")

st.title("Monte Carlo Estimation")
st.markdown("""
This app visualizes the Monte Carlo method for estimating areas.
For circles, we estimate π by counting how many random points fall inside the circle.
For irregular shapes (like a star polygon), we use the same idea: random points are sampled in a bounding box, and we estimate area based on how many land inside the shape.
""")

st.sidebar.header("Parameters")
shape = st.sidebar.selectbox("Choose Shape", ["Circle", "Star Polygon"])
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

if shape == "Star Polygon":
    streamlit_star = streamlitStar(n_points, point_size)
    streamlit_star.visualize()
else:
    streamlit_circle = streamlitCircle(n_points, point_size)
    streamlit_circle.visualize()
