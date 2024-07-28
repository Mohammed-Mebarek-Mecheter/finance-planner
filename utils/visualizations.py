# utils/visualizations.py

import plotly.graph_objects as go
import altair as alt
import pandas as pd
import streamlit as st

@st.cache_data
def plot_salary_growth(salaries, years):
    fig = go.Figure(data=[go.Scatter(x=years, y=salaries, mode='lines+markers', name='Salary Growth')])
    fig.update_layout(title='Salary Growth Over Time',
                      xaxis_title='Year',
                      yaxis_title='Salary',
                      template='plotly_white')
    return fig

@st.cache_data
def plot_expenses(forecasted_expenses, years):
    fig = go.Figure()
    for category in forecasted_expenses.columns:
        fig.add_trace(go.Scatter(x=years, y=forecasted_expenses[category], mode='lines+markers', name=category))
    fig.update_layout(title='Expenses Growth Over Time',
                      xaxis_title='Year',
                      yaxis_title='Expenses',
                      template='plotly_white')
    return fig

@st.cache_data
def plot_investment_simulation(investment_values, years):
    fig = go.Figure(data=[go.Scatter(x=years, y=investment_values, mode='lines+markers', name='Investment Simulation')])
    fig.update_layout(title='Investment Simulation Over Time',
                      xaxis_title='Year',
                      yaxis_title='Investment Value',
                      template='plotly_white')
    return fig

@st.cache_data
def plot_salary_growth_altair(salaries, years):
    data = pd.DataFrame({
        'Year': years,
        'Salary': salaries
    })
    chart = alt.Chart(data).mark_line(point=True).encode(
        x='Year',
        y='Salary'
    ).properties(
        title='Salary Growth Over Time'
    )
    return chart

@st.cache_data
def plot_expenses_altair(forecasted_expenses, years):
    data = pd.DataFrame({'Year': years})
    for category in forecasted_expenses.columns:
        data[category] = forecasted_expenses[category]
    melted_data = data.melt('Year', var_name='Category', value_name='Expenses')
    chart = alt.Chart(melted_data).mark_line(point=True).encode(
        x='Year',
        y='Expenses',
        color='Category'
    ).properties(
        title='Expenses Growth Over Time'
    )
    return chart

@st.cache_data
def plot_investment_simulation_altair(investment_values, years):
    data = pd.DataFrame({
        'Year': years,
        'Investment Value': investment_values
    })
    chart = alt.Chart(data).mark_line(point=True).encode(
        x='Year',
        y='Investment Value'
    ).properties(
        title='Investment Simulation Over Time'
    )
    return chart

@st.cache_data
def plot_stock_data(df):
    """
    Plot stock data using Plotly.

    Args:
    - df (pd.DataFrame): DataFrame containing stock data with 'Open' and 'Close' columns.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Open'], name='Open'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close'))
    fig.update_layout(title='Stock Price Over Time', xaxis_title='Date', yaxis_title='Price')
    return fig

@st.cache_data
def plot_budget_vs_actual(df):
    """
    Plot budget vs. actual spending using Plotly.

    Args:
    - df (pd.DataFrame): DataFrame containing budget, actual, and difference.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Category'], y=df['Budget'], name='Budget'))
    fig.add_trace(go.Bar(x=df['Category'], y=df['Actual'], name='Actual'))
    fig.update_layout(
        barmode='group',
        title='Budget vs. Actual Spending',
        xaxis_title='Category',
        yaxis_title='Amount',
        template='plotly_white'
    )
    return fig

def plot_retirement_scenarios(df):
    """
    Plot retirement scenarios using Plotly.

    Args:
    - df (pd.DataFrame): DataFrame containing simulated savings for different growth rates.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Bar(x=[column], y=df[column], name=column))
    fig.update_layout(
        title='Retirement Savings Scenarios',
        xaxis_title='Growth Rate',
        yaxis_title='Savings at Retirement',
        template='plotly_white'
    )
    return fig

def plot_debt_reduction(df):
    """
    Plot debt reduction progress using Plotly.

    Args:
    - df (pd.DataFrame): DataFrame containing the debt reduction schedule.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure()
    for debt_name in df['Name'].unique():
        debt_data = df[df['Name'] == debt_name]
        fig.add_trace(go.Scatter(x=debt_data.index, y=debt_data['Balance'], mode='lines', name=debt_name))
    fig.update_layout(
        title='Debt Reduction Progress',
        xaxis_title='Time',
        yaxis_title='Balance',
        template='plotly_white'
    )
    return fig

def plot_goal_progress(df):
    """
    Plot goal progress using Plotly.

    Args:
    - df (pd.DataFrame): DataFrame containing the goal progress information.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure()
    for index, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Goal']],
            y=[row['Progress (%)']],
            name=row['Goal'],
            text=[f"{row['Progress (%)']:.2f}%"],
            textposition='auto'
        ))
    fig.update_layout(
        title='Goal Progress',
        xaxis_title='Goals',
        yaxis_title='Progress (%)',
        template='plotly_white'
    )
    return fig

def plot_net_worth(net_worth_data, years):
    """
    Plot net worth over time using Plotly.

    Args:
    - net_worth_data (list of float): List of net worth values over time.
    - years (list of int): List of corresponding years.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure(data=[go.Scatter(x=years, y=net_worth_data, mode='lines+markers', name='Net Worth')])
    fig.update_layout(
        title='Net Worth Over Time',
        xaxis_title='Year',
        yaxis_title='Net Worth',
        template='plotly_white'
    )
    return fig

def plot_investment_growth(investment_growth_data, years):
    """
    Plot investment growth over time using Plotly.

    Args:
    - investment_growth_data (list of float): List of investment growth values over time.
    - years (list of int): List of corresponding years.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure object.
    """
    fig = go.Figure(data=[go.Scatter(x=years, y=investment_growth_data, mode='lines+markers', name='Investment Growth')])
    fig.update_layout(
        title='Investment Growth Over Time',
        xaxis_title='Year',
        yaxis_title='Investment Value',
        template='plotly_white'
    )
    return fig