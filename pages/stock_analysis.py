# pages/stock_analysis.py

import streamlit as st
from utils.api import get_stock_data, get_company_overview, process_time_series_data
from streamlit_plotly_events import plotly_events
import plotly.graph_objs as go
from utils.export import export_to_csv
from utils.pdf_export import export_to_pdf
#from openai_integration import get_stock_advice

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
    st.title("Stock Analysis")

    symbol = st.text_input("Enter a stock symbol (e.g., AAPL for Apple):")

    if symbol:
        with st.spinner("Fetching data..."):
            stock_data = get_stock_data(symbol)
            company_overview = get_company_overview(symbol)

        if "Error Message" in stock_data:
            st.error("Couldn't retrieve data. Please check the stock symbol and try again.")
        else:
            st.success(f"Retrieved data for {symbol}")

            st.subheader("Company Overview")
            st.write(f"Name: {company_overview.get('Name')}")
            st.write(f"Sector: {company_overview.get('Sector')}")
            st.write(f"Industry: {company_overview.get('Industry')}")
            st.write(f"Description: {company_overview.get('Description')}")

            df = process_time_series_data(stock_data)
            if df is not None:
                st.subheader("Stock Price Chart")
                fig = display_chart(df, 'Date', ['Close'], chart_type='line')
                st.plotly_chart(fig)

                st.subheader("Recent Stock Data")
                st.dataframe(df.head())
            else:
                st.error("Failed to process stock data.")

            # Get AI-driven stock advice
            #advice = get_stock_advice(symbol)
            #st.write("Stock Advice:", advice)

            st.header("Export Options")
            csv_filename = st.text_input("Enter CSV Filename", value="stock_report.csv")
            if st.button("Export to CSV"):
                export_to_csv(df, csv_filename)
                st.success(f"Data exported to {csv_filename}")

            pdf_filename = st.text_input("Enter PDF Filename", value="stock_report.pdf")
            if st.button("Export to PDF"):
                export_to_pdf(df, pdf_filename)
                st.success(f"Data exported to {pdf_filename}")

if __name__ == "__main__":
    app()
