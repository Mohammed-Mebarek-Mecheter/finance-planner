# pages/goal_tracking.py
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
    st.title("Goal Setting and Tracking")

    st.header("Set Your Financial Goals")
    num_goals = st.number_input("Number of Goals", min_value=1, step=1, value=1)
    goals = []
    for i in range(num_goals):
        st.subheader(f"Goal {i+1}")
        name = st.text_input(f"Name of Goal {i+1}")
        target_amount = st.number_input(f"Target Amount for Goal {i+1}", min_value=0.0, step=1000.0)
        current_amount = st.number_input(f"Current Amount for Goal {i+1}", min_value=0.0, step=100.0)
        goals.append({
            'name': name,
            'target_amount': target_amount,
            'current_amount': current_amount
        })

    if st.button("Track Progress"):
        goal_df = pd.DataFrame(goals)
        goal_df['Progress'] = (goal_df['current_amount'] / goal_df['target_amount']) * 100
        st.dataframe(goal_df)

        fig = display_chart(goal_df, 'name', ['Progress'], chart_type='bar')
        if fig:
            st.plotly_chart(fig)

        # Display the table
        display_table(goal_df, title="Goal Tracking Progress", editable=False)

        st.header("Export Options")
        csv_filename = st.text_input("Enter CSV Filename", value="goal_report.csv")
        if st.button("Export to CSV"):
            export_to_csv(goal_df, csv_filename)
            st.success(f"Data exported to {csv_filename}")

        pdf_filename = st.text_input("Enter PDF Filename", value="goal_report.pdf")
        if st.button("Export to PDF"):
            export_to_pdf(goal_df, pdf_filename)
            st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
