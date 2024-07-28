# pages/debt_management.py

import streamlit as st
import pandas as pd
from utils.export import export_to_csv
from utils.pdf_export import export_to_pdf
#from openai_integration import get_debt_management_advice
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
    st.title("Debt Management")

    st.header("Input Your Debts")
    num_debts = st.number_input("Number of Debts", min_value=1, step=1, value=1)
    debts = []
    for i in range(num_debts):
        st.subheader(f"Debt {i+1}")
        name = st.text_input(f"Name of Debt {i+1}")
        balance = st.number_input(f"Balance of Debt {i+1}", min_value=0.0, step=100.0)
        interest_rate = st.number_input(f"Interest Rate of Debt {i+1} (%)", min_value=0.0, step=0.1)
        monthly_payment = st.number_input(f"Monthly Payment for Debt {i+1}", min_value=0.0, step=10.0)
        debts.append({
            'name': name,
            'balance': balance,
            'interest_rate': interest_rate,
            'monthly_payment': monthly_payment
        })

    if st.button("Track Payments"):
        debt_df = pd.DataFrame(debts)
        st.dataframe(debt_df)

        # Debt reduction over time (e.g., snowball method)
        debt_reduction = pd.DataFrame({
            'Month': range(1, 25),
            **{f"Debt {i+1}": [debt['balance'] - (debt['monthly_payment'] * month) for month in range(1, 25)] for i, debt in enumerate(debts)}
        })
        st.dataframe(debt_reduction)
        fig = display_chart(debt_reduction, 'Month', debt_reduction.columns[1:], chart_type='line')
        st.plotly_chart(fig)

        # Display the table
        #display_table(debt_reduction, title="Debt Reduction Schedule", editable=False)

        # Get AI-driven debt management advice
        #advice = get_debt_management_advice(debts)
        #st.write("Debt Management Advice:", advice)

        st.header("Export Options")
        csv_filename = st.text_input("Enter CSV Filename", value="debt_report.csv")
        if st.button("Export to CSV"):
            export_to_csv(debt_df, csv_filename)
            st.success(f"Data exported to {csv_filename}")

        pdf_filename = st.text_input("Enter PDF Filename", value="debt_report.pdf")
        if st.button("Export to PDF"):
            export_to_pdf(debt_df, pdf_filename)
            st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
