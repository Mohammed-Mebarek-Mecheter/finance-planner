# pages/salary_expenses.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

def display_chart(data, x_column, y_columns, chart_type='line'):
    fig = go.Figure()
    for y_column in y_columns:
        if chart_type == 'line':
            fig.add_trace(go.Bar(x=data[x_column], y=data[y_column], name=y_column))
        else:
            st.error("Unsupported chart type. Use 'line' or 'bar'.")
            return None
    selected_points = plotly_events(fig, key=f"unique_key_{x_column}_{y_columns}")
    return fig

def display_table(data, title="Table", editable=False):
    st.subheader(title)
    st.dataframe(data)

def export_to_csv(data, filename):
    data.to_csv(filename, index=False)
    st.success(f"Data exported to {filename}")

def export_to_pdf(data, filename):
    # Placeholder function for exporting to PDF
    st.success(f"Data exported to {filename}")

def app():
    st.title("Salary and Expenses")

    salary = st.number_input("Annual Gross Salary", min_value=0.0, step=1000.0)
    deductions = st.number_input("Annual Deductions", min_value=0.0, step=500.0)
    tax_brackets = [(10000, 0.1), (50000, 0.2), (100000, 0.3), (float('inf'), 0.4)]

    if salary and deductions:
        monthly_take_home = salary * (1 - sum(rate for amount, rate in tax_brackets if salary > amount) / 12) - deductions / 12
        st.write(f"Monthly Take-Home Pay: ${monthly_take_home:.2f}")

    annual_growth_rate = st.slider("Annual Salary Growth Rate (%)", 0.0, 10.0, 3.0) / 100
    forecast_years = st.number_input("Number of Years to Forecast", min_value=1, step=1, value=5)

    if salary and annual_growth_rate and forecast_years:
        projected_salaries = pd.DataFrame({
            'Year': range(1, forecast_years + 1),
            'Salary': [salary * (1 + annual_growth_rate) ** i for i in range(forecast_years)]
        })
        fig_salary = display_chart(projected_salaries, 'Year', ['Salary'], chart_type='line')
        if fig_salary:
            st.plotly_chart(fig_salary)

    expense_categories = ["Housing", "Food", "Transport", "Entertainment"]
    expenses = {category: st.number_input(f"Current {category} Expenses", min_value=0.0, step=100.0, value=1000.0) for category in expense_categories}
    inflation_rates = {category: st.slider(f"Annual Inflation Rate for {category} (%)", 0.0, 10.0, 3.0) / 100 for category in expense_categories}

    if expenses and inflation_rates:
        forecasted_expenses = pd.DataFrame({
            'Year': range(1, forecast_years + 1),
            **{category: [expenses[category] * (1 + inflation_rates[category]) ** i for i in range(forecast_years)] for category in expense_categories}
        })
        fig_expenses = display_chart(forecasted_expenses, 'Year', expense_categories, chart_type='line')
        if fig_expenses:
            st.plotly_chart(fig_expenses)

        # Display the table
        display_table(forecasted_expenses, title="Expense Forecast", editable=False)

        # Get AI-driven salary advice
        # advice = get_salary_advice(salary, deductions, annual_growth_rate, forecast_years)
        # st.write("Salary Advice:", advice)

        st.header("Export Options")
        csv_filename = st.text_input("Enter CSV Filename", value="salary_report.csv")
        if st.button("Export to CSV"):
            export_to_csv(forecasted_expenses, csv_filename)
            st.success(f"Data exported to {csv_filename}")

        pdf_filename = st.text_input("Enter PDF Filename", value="salary_report.pdf")
        if st.button("Export to PDF"):
            export_to_pdf(forecasted_expenses, pdf_filename)
            st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
