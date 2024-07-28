# utils/calculations.py

import numpy as np
import pandas as pd

def calculate_take_home_pay(salary, deductions, tax_brackets):
    """
    Calculate monthly take-home pay after taxes and deductions.

    Args:
    - salary (float): Annual gross salary.
    - deductions (float): Total annual deductions.
    - tax_brackets (list of tuples): Tax brackets as (income_threshold, tax_rate).

    Returns:
    - float: Monthly take-home pay.
    - dict: Detailed breakdown of taxes and deductions.
    """
    taxable_income = salary - deductions
    taxes = 0
    for threshold, rate in tax_brackets:
        if taxable_income > threshold:
            taxes += (taxable_income - threshold) * rate
            taxable_income = threshold

    annual_take_home = salary - taxes - deductions
    monthly_take_home = annual_take_home / 12

    breakdown = {
        "gross_salary": salary,
        "deductions": deductions,
        "taxes": taxes,
        "net_salary": annual_take_home
    }

    return monthly_take_home, breakdown

def forecast_salary_growth(salary, annual_growth_rate, raises, bonuses, years):
    """
    Forecast salary growth over a number of years with raises and bonuses.

    Args:
    - salary (float): Current annual salary.
    - annual_growth_rate (float): Expected annual growth rate as a decimal.
    - raises (dict): Yearly raises as {year: raise_amount}.
    - bonuses (dict): Yearly bonuses as {year: bonus_amount}.
    - years (int): Number of years to forecast.

    Returns:
    - pd.Series: Projected annual salaries over the specified years.
    """
    salary_series = pd.Series([salary] * years)
    for year in range(years):
        if year in raises:
            salary_series[year] += raises[year]
        if year in bonuses:
            salary_series[year] += bonuses[year]
        salary_series[year] *= (1 + annual_growth_rate)
    return salary_series

def forecast_expenses(expenses, inflation_rates, categories, years):
    """
    Forecast expenses growth over a number of years due to inflation.

    Args:
    - expenses (dict): Current annual expenses by category.
    - inflation_rates (dict): Annual inflation rates by category as a decimal.
    - categories (list): List of expense categories.
    - years (int): Number of years to forecast.

    Returns:
    - pd.DataFrame: Projected annual expenses for each category over the specified years.
    """
    forecasted_expenses = pd.DataFrame({category: [expenses[category]] * years for category in categories})
    for year in range(1, years):
        for category in categories:
            forecasted_expenses.loc[year, category] = forecasted_expenses.loc[year-1, category] * (1 + inflation_rates[category])
    return forecasted_expenses

def simulate_investments(initial_investment, investment_options, portfolio, years):
    """
    Simulate investment growth over a number of years with a diversified portfolio.

    Args:
    - initial_investment (float): Initial investment amount.
    - investment_options (dict): Expected annual returns for different investments.
    - portfolio (dict): Portfolio distribution as a percentage for each investment.
    - years (int): Number of years to simulate.

    Returns:
    - list of float: Simulated investment values over the specified years.
    """
    investment_value = initial_investment
    investment_values = [investment_value]

    for year in range(1, years + 1):
        growth = sum(investment_value * portfolio[investment] * investment_options[investment] for investment in portfolio)
    investment_value += growth
    investment_values.append(investment_value)

    return investment_values

def calculate_budget_vs_actual(budget, actual):
    """
    Calculate the difference between budgeted and actual spending.

    Args:
    - budget (dict): Budgeted amounts by category.
    - actual (dict): Actual spending amounts by category.

    Returns:
    - pd.DataFrame: DataFrame containing budget, actual, and difference.
    """
    categories = budget.keys()
    data = {
        "Category": categories,
        "Budget": [budget[cat] for cat in categories],
        "Actual": [actual.get(cat, 0) for cat in categories],
        "Difference": [actual.get(cat, 0) - budget[cat] for cat in categories]
    }
    return pd.DataFrame(data)

def calculate_retirement_savings(current_savings, annual_contribution, years_to_retirement, annual_growth_rate):
    """
    Calculate the future value of retirement savings.

    Args:
    - current_savings (float): Current savings amount.
    - annual_contribution (float): Annual contribution amount.
    - years_to_retirement (int): Number of years until retirement.
    - annual_growth_rate (float): Expected annual growth rate as a decimal.

    Returns:
    - float: Estimated savings at retirement.
    """
    future_value = current_savings
    for _ in range(years_to_retirement):
        future_value = (future_value + annual_contribution) * (1 + annual_growth_rate)
    return future_value

def simulate_retirement_scenarios(current_savings, annual_contribution, years_to_retirement, annual_growth_rates):
    """
    Simulate different retirement scenarios based on varying growth rates.

    Args:
    - current_savings (float): Current savings amount.
    - annual_contribution (float): Annual contribution amount.
    - years_to_retirement (int): Number of years until retirement.
    - annual_growth_rates (list of float): List of different annual growth rates.

    Returns:
    - pd.DataFrame: DataFrame containing the simulated savings for each growth rate.
    """
    scenarios = {}
    for rate in annual_growth_rates:
        savings = calculate_retirement_savings(current_savings, annual_contribution, years_to_retirement, rate)
        scenarios[f"{rate * 100}% Growth"] = savings
    return pd.DataFrame(scenarios, index=[0])

def track_debt_payments(debts):
    """
    Track debt payments and calculate remaining balances.

    Args:
    - debts (list of dict): List of debts with 'name', 'balance', 'interest_rate', and 'monthly_payment'.

    Returns:
    - pd.DataFrame: DataFrame containing the debt tracking information.
    """
    debt_data = []
    for debt in debts:
        balance = debt['balance']
        interest_rate = debt['interest_rate'] / 100
        monthly_payment = debt['monthly_payment']
        monthly_interest = balance * interest_rate / 12
        principal_payment = monthly_payment - monthly_interest
        new_balance = balance - principal_payment

        debt_data.append({
            'Name': debt['name'],
            'Balance': balance,
            'Monthly Payment': monthly_payment,
            'Monthly Interest': monthly_interest,
            'Principal Payment': principal_payment,
            'New Balance': new_balance
        })

    return pd.DataFrame(debt_data)

def debt_snowball_method(debts):
    """
    Apply the debt snowball method for debt reduction.

    Args:
    - debts (list of dict): List of debts with 'name', 'balance', 'interest_rate', and 'monthly_payment'.

    Returns:
    - pd.DataFrame: DataFrame containing the debt snowball payment schedule.
    """
    sorted_debts = sorted(debts, key=lambda x: x['balance'])
    payment_schedule = []

    while any(debt['balance'] > 0 for debt in sorted_debts):
        for debt in sorted_debts:
            if debt['balance'] > 0:
                balance = debt['balance']
                interest_rate = debt['interest_rate'] / 100
                monthly_payment = debt['monthly_payment']
                monthly_interest = balance * interest_rate / 12
                principal_payment = monthly_payment - monthly_interest
                new_balance = balance - principal_payment
                debt['balance'] = new_balance if new_balance > 0 else 0

                payment_schedule.append({
                    'Name': debt['name'],
                    'Balance': balance,
                    'Monthly Payment': monthly_payment,
                    'Monthly Interest': monthly_interest,
                    'Principal Payment': principal_payment,
                    'New Balance': debt['balance']
                })

                if debt['balance'] == 0:
                    for d in sorted_debts:
                        if d['balance'] > 0:
                            d['monthly_payment'] += monthly_payment
                            break

    return pd.DataFrame(payment_schedule)

def calculate_goal_progress(goals, savings):
    """
    Calculate progress towards financial goals.

    Args:
    - goals (list of dict): List of financial goals with 'name', 'target_amount', and 'current_amount'.
    - savings (float): Current savings amount.

    Returns:
    - pd.DataFrame: DataFrame containing the goal progress information.
    """
    goal_data = []
    for goal in goals:
        goal_name = goal['name']
        target_amount = goal['target_amount']
        current_amount = goal['current_amount']
        remaining_amount = target_amount - current_amount
        progress = (current_amount / target_amount) * 100

        goal_data.append({
            'Goal': goal_name,
            'Target Amount': target_amount,
            'Current Amount': current_amount,
            'Remaining Amount': remaining_amount,
            'Progress (%)': progress
        })

    return pd.DataFrame(goal_data)

def generate_csv_report(data, filename):
    """
    Generate a CSV report.

    Args:
    - data (pd.DataFrame): DataFrame containing the report data.
    - filename (str): The name of the CSV file.

    Returns:
    - None
    """
    data.to_csv(filename, index=False)

def generate_pdf_report(data, filename):
    """
    Generate a PDF report.

    Args:
    - data (pd.DataFrame): DataFrame containing the report data.
    - filename (str): The name of the PDF file.

    Returns:
    - None
    """
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Financial Report', 0, 1, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(10)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()

    for column in data.columns:
        pdf.chapter_title(column)
        body = "\n".join(data[column].astype(str).values)
        pdf.chapter_body(body)

    pdf.output(filename)