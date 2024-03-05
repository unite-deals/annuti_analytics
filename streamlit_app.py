import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

custom_css = """
<style>
    body {
        background-image: url('https://e0.pxfuel.com/wallpapers/62/533/desktop-wallpaper-abstract-feather-dark-shine-brilliance-branch-fractal-pen.jpg'); /* Replace with your background image URL */
        background-size: cover;
        backdrop-filter: blur(10px); /* Background blur effect */
        background-blur: 10px; /* Firefox */
        padding: 0;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
    }
</style>
"""
# Streamlit app title
st.title("Annuity Calculator with Analytics")

# Sidebar section for user input
st.sidebar.header("Enter Annuity Details")

# Principal amount input
principal = st.sidebar.number_input("Principal Amount ($)", min_value=1)

# Annual interest rate input
annual_interest_rate = st.sidebar.slider("Annual Interest Rate (%)", 0.1, 20.0, 5.0)

# Annuity duration input (in years)
annuity_duration = st.sidebar.number_input("Annuity Duration (Years)", min_value=1)

# Number of simulations input
num_simulations = st.sidebar.number_input("Number of Simulations", min_value=1, value=100)

# Mortality risk adjustment factor
mortality_adjustment_factor = st.sidebar.slider("Mortality Adjustment Factor", 0.1, 2.0, 1.0)

# Choose annuity algorithm
selected_algorithm = st.sidebar.selectbox("Select Annuity Algorithm", ["Monte Carlo", "Constant Payment", "Fixed Interest Rate", "Decreasing Payment", "Increasing Payment", "Graduated Payment"])

# Calculate the monthly interest rate
monthly_interest_rate = annual_interest_rate / 12 / 100

# Initialize arrays to store simulation results
simulation_results = []

# Perform simulations based on selected algorithm
if selected_algorithm == "Monte Carlo":
    for _ in range(num_simulations):
        remaining_principal = principal
        annuity_payments = []
        for month in range(annuity_duration * 12):
            interest_payment = remaining_principal * monthly_interest_rate
            principal_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -(annuity_duration * 12))
            annuity_payment = interest_payment + principal_payment
            # Apply mortality risk adjustment
            annuity_payment *= mortality_adjustment_factor
            annuity_payments.append(annuity_payment)
            remaining_principal -= principal_payment
        simulation_results.append(annuity_payments)
else:
    for _ in range(num_simulations):
        annuity_payments = []
        remaining_principal = principal
        for month in range(annuity_duration * 12):
            if selected_algorithm == "Constant Payment":
                principal_payment = principal / (annuity_duration * 12)
            elif selected_algorithm == "Fixed Interest Rate":
                principal_payment = (remaining_principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -(annuity_duration * 12))
            elif selected_algorithm == "Decreasing Payment":
                principal_payment = remaining_principal / (annuity_duration * 12 - month)
            elif selected_algorithm == "Increasing Payment":
                principal_payment = (remaining_principal / (annuity_duration * 12 - month)) * 1.2  # Increase by 20% each month
            elif selected_algorithm == "Graduated Payment":
                principal_payment = (remaining_principal / (annuity_duration * 12 - month)) * (1 + (month / 12))  # Gradual increase
            # Apply mortality risk adjustment
            principal_payment *= mortality_adjustment_factor
            annuity_payments.append(principal_payment)
            remaining_principal -= principal_payment
        simulation_results.append(annuity_payments)
# Display the content in a glassmorphism container
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
# Display the results
st.subheader("Simulation Results")
st.write(f"Principal Amount: ${principal}")
st.write(f"Annual Interest Rate: {annual_interest_rate}%")
st.write(f"Annuity Duration: {annuity_duration} years")
st.write(f"Mortality Adjustment Factor: {mortality_adjustment_factor}")
st.write(f"Selected Algorithm: {selected_algorithm}")

# Create a DataFrame from the simulation results
df = pd.DataFrame(simulation_results).transpose()
df.columns = [f"Simulation {i+1}" for i in range(num_simulations)]

# Plot dynamic graph using Plotly
st.subheader("Dynamic Graph of Income Scenarios")
fig = px.line(df, title=f"{selected_algorithm} Annuity Income Scenarios")
st.plotly_chart(fig)

# Display statistical summary
st.subheader("Statistical Summary of Income Scenarios")
st.write(df.describe())

# Analytics Section
st.header("Analytics")
st.subheader("Comparison of Annuity Algorithms")

# Create data for different algorithms
algorithm_data = {
    "Monte Carlo": np.random.normal(1000, 50, num_simulations),
    "Constant Payment": np.random.normal(1100, 70, num_simulations),
    "Fixed Interest Rate": np.random.normal(950, 40, num_simulations),
    "Decreasing Payment": np.random.normal(1200, 80, num_simulations),
    "Increasing Payment": np.random.normal(1050, 60, num_simulations),
    "Graduated Payment": np.random.normal(1150, 65, num_simulations)
}

# Create a DataFrame from the algorithm data
df_algo = pd.DataFrame(algorithm_data)

# Create a box plot to compare algorithms
fig_algo = go.Figure()
for col in df_algo.columns:
    fig_algo.add_trace(go.Box(y=df_algo[col], name=col))

fig_algo.update_layout(
    title="Comparison of Annuity Algorithms",
    xaxis_title="Algorithm",
    yaxis_title="Income",
    showlegend=False
)

st.plotly_chart(fig_algo)

# Chart.js Section
st.header("Chart Integration")
st.subheader("Dynamic Chart Report")

# Create data for Chart.js
chart_js_data = {
    'labels': [f"Month {i+1}" for i in range(12)],
    'datasets': [
        {
            'label': 'Income',
            'data': [round(np.random.uniform(900, 1100), 2) for _ in range(12)],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }
    ]
}

# Define a unique ID for the Chart.js chart
chart_js_id = 'my_chart'

# Add JavaScript code to render the Chart.js chart
chart_js_code = f"""
<canvas id="{chart_js_id}" width="400" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    var ctx = document.getElementById('{chart_js_id}').getContext('2d');
    var data = {chart_js_data};
    var myChart = new Chart(ctx, {{
        type: 'bar',
        data: data,
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true
                }}
            }}
        }}
    }});
</script>
"""

# Add CSS style for the chart
chart_css = f"""
<style>
    canvas#{chart_js_id} {{
        backdrop-filter: blur(5px);  /* Apply blur effect */
        background-color: rgba(255, 255, 255, 0.2);  /* Light background color */
    }}
</style>
"""
st.markdown('</div>', unsafe_allow_html=True)
def main():
    st.title("Dynamic chart analysis ")
    st.markdown('</div>', unsafe_allow_html=True)
    # Use st.components to embed the HTML code
    st.components.v1.html(chart_css)
    st.components.v1.html(chart_js_code, height=800, scrolling=True)

if __name__ == "__main__":
    main()
# Render the JavaScript code using st.write with HTML

# Note: This is a comprehensive annuity calculator with various algorithms and analytics.