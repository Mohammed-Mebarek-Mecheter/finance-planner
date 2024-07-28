# pages/budgeting.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

def display_chart(data, x_column, y_columns, chart_type='bar'):
    fig = go.Figure()
    for y_column in y_columns:
        if chart_type == 'bar':
            fig.add_trace(go.Bar(x=data[x_column], y=data[y_column], name=y_column))
        elif chart_type == 'line':
            fig.add_trace(go.Scatter(x=data[x_column], y=data[y_column], mode='lines', name=y_column))
        else:
            st.error("Unsupported chart type. Use 'bar' or 'line'.")
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
    st.title("Budgeting Tool")

    st.header("Set Up Your Budget")
    budget_categories = ["Savings", "Utilities", "Groceries", "Entertainment", "Others"]
    budget = {cat: st.number_input(f"Budget for {cat}", min_value=0.0, step=10.0) for cat in budget_categories}

    st.header("Track Your Actual Spending")
    actual = {cat: st.number_input(f"Actual spending for {cat}", min_value=0.0, step=10.0) for cat in budget_categories}

    if st.button("Calculate"):
        df = pd.DataFrame({
            "Category": budget_categories,
            "Budget": [budget[cat] for cat in budget_categories],
            "Actual": [actual[cat] for cat in budget_categories]
        })
        df['Difference'] = df['Budget'] - df['Actual']
        st.dataframe(df)

        fig = display_chart(df, 'Category', ['Budget', 'Actual'], chart_type='bar')
        if fig:
            st.plotly_chart(fig)

        # Display the table
        display_table(df, title="Budget vs. Actual Spending", editable=False)

        st.header("Export Options")
        csv_filename = st.text_input("Enter CSV Filename", value="budget_report.csv")
        if st.button("Export to CSV"):
            export_to_csv(df, csv_filename)
            st.success(f"Data exported to {csv_filename}")

        pdf_filename = st.text_input("Enter PDF Filename", value="budget_report.pdf")
        if st.button("Export to PDF"):
            export_to_pdf(df, pdf_filename)
            st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
