import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt


def preprocess_data(df) -> pd.DataFrame:
    df['mese'] = pd.Categorical(
        df['mese'],
        categories=[
            'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
            'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
        ],
        ordered=True
    )
    # convert importo to float
    df['importo'] = df['importo'].str.replace(',', '.').astype(float)
    return df


# App Layout
st.title("Personal Budget Dashboard")

# upload csv
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    data = preprocess_data(data)

    # Display the metrics of the current month
    current_month = data['mese'].max()
    current_month_data = data.query('mese == @current_month')

    # Separate income and expenses
    total_expense = current_month_data.query('categoria != "Stipendio"')['importo'].sum()
    total_income = current_month_data.query('categoria == "Stipendio"')['importo'].sum()

    # Filter data for past months
    past_months_data = data.query('mese != @current_month')

    # Calculate past expenses and income
    mean_expense = past_months_data.query('categoria != "Stipendio"')['importo'].mean()
    mean_income = past_months_data.query('categoria == "Stipendio"')['importo'].mean()

    # split into two columns
    col1, col2 = st.columns(2)
    col1.metric("Total Expense", f"{total_expense:.2f} €", delta=f"{total_expense - mean_expense:.2f} €")
    col2.metric("Total Income", f"{total_income:.2f} €", delta=f"{total_income - mean_income:.2f} €")

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

    st.subheader("Expenses")
    # Exclude 'Stipendio' category
    expenses = filtered_data[filtered_data['categoria'] != 'Stipendio']

    st.subheader(f"Total Expense by Category in {', '.join(selected_months)}")
    st.bar_chart(expenses.groupby('categoria')['importo'].sum())

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
