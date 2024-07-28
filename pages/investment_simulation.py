# pages/investment_simulation.py

import streamlit as st
import pandas as pd
from utils.export import export_to_csv
from utils.pdf_export import export_to_pdf
#from openai_integration import get_investment_advice
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
    st.title("Investment Simulation")

    initial_investment = st.number_input("Initial Investment Amount", min_value=0.0, step=1000.0)
    years = st.number_input("Number of Years to Simulate", min_value=1, step=1)

    investment_options = {
        "Stocks": st.slider("Expected Annual Return for Stocks (%)", -10.0, 20.0, 7.0) / 100,
        "Bonds": st.slider("Expected Annual Return for Bonds (%)", -10.0, 10.0, 3.0) / 100,
        "Mutual Funds": st.slider("Expected Annual Return for Mutual Funds (%)", -10.0, 15.0, 5.0) / 100
    }

    portfolio = {
        "Stocks": st.slider("Percentage of Portfolio in Stocks", 0, 100, 50),
        "Bonds": st.slider("Percentage of Portfolio in Bonds", 0, 100, 30),
        "Mutual Funds": st.slider("Percentage of Portfolio in Mutual Funds", 0, 100, 20)
    }

    total_percentage = sum(portfolio.values())
    portfolio = {k: v / total_percentage for k, v in portfolio.items()}

    if st.button("Simulate Investment"):
        # Simulate investments here and create a DataFrame
        investment_values = pd.DataFrame({
            'Year': range(1, years + 1),
            'Value': [initial_investment * (1 + investment_options['Stocks']) ** i for i in range(years)]
        })
        st.plotly_chart(display_chart(investment_values, 'Year', ['Value'], chart_type='line'))

        # Display the table
        #display_table(investment_values, title="Investment Simulation Results", editable=False)

        # Get AI-driven investment advice
        #advice = get_investment_advice(initial_investment, investment_options, portfolio, years)
        #st.write("Investment Advice:", advice)

        st.header("Export Options")
        csv_filename = st.text_input("Enter CSV Filename", value="investment_report.csv")
        if st.button("Export to CSV"):
            export_to_csv(investment_values, csv_filename)
            st.success(f"Data exported to {csv_filename}")

        pdf_filename = st.text_input("Enter PDF Filename", value="investment_report.pdf")
        if st.button("Export to PDF"):
            export_to_pdf(investment_values, pdf_filename)
            st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
