import streamlit as st
import pandas as pd
from src.utils.plot_utils import pie_plot, display_metrics
from src.utils.data_utils import preprocess_data

# App Layout
st.title("Personal Budget Dashboard")

# upload csv
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    data = preprocess_data(data)

    display_metrics(data)

    # Filters
    st.sidebar.header("Filters")
    selected_months = st.sidebar.multiselect(
        "Select Month(s):", data['mese'].unique(), default=data['mese'].unique()
    )
    selected_categories = st.sidebar.multiselect(
        "Select Category(s):", data['categoria'].unique(), default=data['categoria'].unique()
    )

    # Apply filters
    filtered_data = data[
        (data['mese'].isin(selected_months)) &
        (data['categoria'].isin(selected_categories))
    ]

    # Display filtered data in sidebar
    with st.sidebar:
        st.header("Filtered Data")
        st.write(filtered_data)

    # Visualizations
    st.header("Your Personal Budget Dashboard")
    # Exclude 'Stipendio' category
    expenses = filtered_data[filtered_data['categoria'] != 'Stipendio']

    st.subheader(f"Total Expense by Category in {', '.join(selected_months)}")
    grouped_expenses = expenses.groupby('categoria')['importo'].sum()
    # Create a pie chart
    pie_plot(grouped_expenses)
    # Total Expense by Month
    st.subheader("Total Expense by Month")

    # Group by 'mese' and calculate the total expense
    monthly_expenses = expenses.groupby('mese')['importo'].sum()
    st.line_chart(monthly_expenses)

    st.subheader("Income")
    # Include only 'Stipendio' category
    income = filtered_data[filtered_data['categoria'] == 'Stipendio']

    # Total Income by Month
    st.subheader("Total Income by Month")

    # Group by 'mese' and calculate the total income
    monthly_income = income.groupby('mese')['importo'].sum()
    st.line_chart(monthly_income)

else:
    st.info("Please upload the budget data.")
