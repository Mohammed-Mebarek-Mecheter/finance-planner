# utils/helpers.py

def get_tax_rate(tax_brackets, income):
    """
    Determine the tax rate based on income using tax brackets.

    Args:
    - tax_brackets (list of tuples): Tax brackets as (income_threshold, tax_rate).
    - income (float): Annual income.

    Returns:
    - float: Effective tax rate.
    """
    for threshold, rate in tax_brackets:
        if income <= threshold:
            return rate
    return tax_brackets[-1][1]  # Return the highest rate if income exceeds all thresholds

def inflation_adjustment(amount, inflation_rate, years):
    """
    Adjust an amount for inflation over a number of years.

    Args:
    - amount (float): Initial amount.
    - inflation_rate (float): Annual inflation rate as a decimal.
    - years (int): Number of years for adjustment.

    Returns:
    - float: Adjusted amount after the specified number of years.
    """
    return amount * (1 + inflation_rate) ** years
