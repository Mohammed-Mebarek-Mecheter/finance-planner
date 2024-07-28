# pages/retirement_planning.py

import streamlit as st
import pandas as pd
from utils.export import export_to_csv
from utils.pdf_export import export_to_pdf
#from openai_integration import get_retirement_advice
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

def display_chart(data, x_column, y_columns, chart_type='line'):
    fig = go.Figure()
    for y_column in y_columns:
        if chart_type == 'line':
            fig.add_trace(go.Scatter(x=data[x_column], y=data[y_column], mode='lines', name=y_column))
        elif chart_type == 'bar':
            fig.add_trace(go.Bar(x=data[x_column], y=data[y_column], name=y_column))
        else:
            st.error("Unsupported chart type. Use 'line' or 'bar'.")
            return None
    selected_points = plotly_events(fig, key=f"unique_key_{x_column}_{y_columns}")
    return fig

def app():
    st.title("Retirement Planning")

    st.header("Estimate Your Retirement Savings")
    current_savings = st.number_input("Current Savings", min_value=0.0, step=1000.0)
    annual_contribution = st.number_input("Annual Contribution", min_value=0.0, step=1000.0)
    years_to_retirement = st.number_input("Years to Retirement", min_value=1, step=1)
    annual_growth_rate = st.slider("Expected Annual Growth Rate (%)", 0.0, 15.0, 5.0) / 100

    if st.button("Calculate Retirement Savings"):
        future_savings = current_savings * (1 + annual_growth_rate) ** years_to_retirement + annual_contribution * (((1 + annual_growth_rate) ** years_to_retirement - 1) / annual_growth_rate)
        st.write(f"Estimated Savings at Retirement: ${future_savings:,.2f}")

    st.header("Simulate Different Retirement Scenarios")
    growth_rates = [0.03, 0.05, 0.07, 0.1]
    if st.button("Simulate Scenarios"):
        scenarios = pd.DataFrame({
            'Year': range(1, years_to_retirement + 1),
            **{f"Growth Rate {rate*100}%": [current_savings * (1 + rate) ** i + annual_contribution * (((1 + rate) ** i - 1) / rate) for i in range(years_to_retirement)] for rate in growth_rates}
        })
        st.dataframe(scenarios)
        fig = display_chart(scenarios, 'Year', scenarios.columns[1:], chart_type='line')
        st.plotly_chart(fig)

        # Get AI-driven retirement advice
        #advice = get_retirement_advice(current_savings, annual_contribution, years_to_retirement, annual_growth_rate)
        #st.write("Retirement Advice:", advice)

        st.header("Export Options")
        csv_filename = st.text_input("Enter CSV Filename", value="retirement_report.csv")
        if st.button("Export to CSV"):
            export_to_csv(scenarios, csv_filename)
            st.success(f"Data exported to {csv_filename}")

        pdf_filename = st.text_input("Enter PDF Filename", value="retirement_report.pdf")
        if st.button("Export to PDF"):
            export_to_pdf(scenarios, pdf_filename)
            st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
