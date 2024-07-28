# pages/admin.py

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from utils.data_storage import get_user, get_user_activity

def create_aggrid_table(data: pd.DataFrame, editable: bool = False, selectable: str = 'single'):
    """
    Create an interactive AgGrid table in Streamlit.

    Parameters:
    - data (pd.DataFrame): The data to display in the table.
    - editable (bool): Allow cells to be editable.
    - selectable (str): Type of row selection ('single' or 'multiple').

    Returns:
    - dict: Selected rows data.
    """
    options_builder = GridOptionsBuilder.from_dataframe(data)
    options_builder.configure_pagination(paginationAutoPageSize=True)
    options_builder.configure_side_bar()
    options_builder.configure_selection(selection_mode=selectable, use_checkbox=True)
    options_builder.configure_default_column(editable=editable)

    grid_options = options_builder.build()

    grid_response = AgGrid(
        data,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=True
    )

    selected_rows = grid_response['selected_rows']
    return selected_rows

def display_table(data: pd.DataFrame, title: str = "Interactive Table", editable: bool = False, selectable: str = 'single'):
    """
    Display an AgGrid table with a title in Streamlit.

    Parameters:
    - data (pd.DataFrame): The data to display in the table.
    - title (str): The title to display above the table.
    - editable (bool): Allow cells to be editable.
    - selectable (str): Type of row selection ('single' or 'multiple').
    """
    st.subheader(title)
    selected_rows = create_aggrid_table(data, editable, selectable)
    st.write("Selected Rows:", selected_rows)

def app():
    st.title("Admin Page")

    st.header("User Management")
    users = get_user()
    user_df = pd.DataFrame(users)

    if not user_df.empty:
        display_table(user_df, title="Registered Users", editable=False, selectable='multiple')

        # Additional user activity and information
        st.header("User Activity")
        selected_user = st.selectbox("Select a user to view activity", user_df['username'].unique())

        if selected_user:
            user_activity = get_user_activity(selected_user)
            if user_activity:
                activity_df = pd.DataFrame(user_activity)
                st.subheader(f"Activity for {selected_user}")
                st.dataframe(activity_df)
            else:
                st.write(f"No activity found for {selected_user}.")
    else:
        st.write("No users found.")

if __name__ == "__main__":
    app()
