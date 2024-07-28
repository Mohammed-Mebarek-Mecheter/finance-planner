# utils/__init__.py

from .calculations import calculate_take_home_pay, forecast_salary_growth, forecast_expenses
from .visualizations import plot_salary_growth, plot_expenses, plot_investment_simulation
from .helpers import get_tax_rate, inflation_adjustment

__all__ = [
    "calculate_take_home_pay",
    "forecast_salary_growth",
    "forecast_expenses",
    "plot_salary_growth",
    "plot_expenses",
    "plot_investment_simulation",
    "get_tax_rate",
    "inflation_adjustment"
]
