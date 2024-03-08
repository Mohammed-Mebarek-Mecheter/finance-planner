import streamlit as st

def main():
    st.title("Salary and Expenses Calculator")
    st.header("Calculate Your Monthly Budget")

    # Interactive widgets for input
    salary = st.number_input("Enter Your Monthly Salary:", min_value=0.0, step=100.0)
    rent = st.number_input("Enter Your Monthly Rent Expense:", min_value=0.0, step=100.0)
    groceries = st.number_input("Enter Your Monthly Grocery Expense:", min_value=0.0, step=100.0)
    utilities = st.number_input("Enter Your Monthly Utilities Expense:", min_value=0.0, step=100.0)
    other_expenses = st.number_input("Enter Your Other Monthly Expenses:", min_value=0.0, step=100.0)

    # Calculate total expenses
    total_expenses = rent + groceries + utilities + other_expenses

    # Calculate remaining budget
    remaining_budget = salary - total_expenses

    # Displaying data
    st.subheader("Budget Summary")
    st.write(f"Total Monthly Expenses: ${total_expenses}")
    st.write(f"Remaining Budget: ${remaining_budget}")

    # Display a message based on budget
    if remaining_budget >= 0:
        st.success("You're within your budget!")
    else:
        st.error("You've exceeded your budget!")

if __name__ == "__main__":
    main()
