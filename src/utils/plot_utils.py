import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def display_metrics(data: pd.DataFrame):
    # Display the metrics of the current month
    current_month = data['mese'].max()
    current_month_data = data.query('mese == @current_month')

    # Separate income and expenses
    total_expense = current_month_data.query('categoria != "Stipendio"')['importo'].sum()
    total_income = current_month_data.query('categoria == "Stipendio"')['importo'].sum()

    # Filter data for past months
    past_months_data = data.query('mese != @current_month')

    # Calculate past expenses and income
    mean_expense = past_months_data.query('categoria != "Stipendio"')['importo'].mean() or 0.0
    mean_income = past_months_data.query('categoria == "Stipendio"')['importo'].mean() or 0.0
    mean_savings = mean_income - mean_expense

    # split into two columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expense", f"{total_expense:.2f} €", delta=f"{total_expense - mean_expense:.2f} €")
    col2.metric("Total Income", f"{total_income:.2f} €", delta=f"{total_income - mean_income:.2f} €")
    col3.metric("Savings", f"{total_income - total_expense:.2f} €", delta=f"{mean_savings:.2f} €")

    # display as metric the numer of transactions in expenses
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", current_month_data.query('categoria != "Stipendio"').shape[0])
    # display as metric the numer of transactions in income
    col2.metric("Total Income Transactions", current_month_data.query('categoria == "Stipendio"').shape[0])





def pie_plot(grouped_expenses: pd.DataFrame):
    bg_color = "#0E1117"
    text_color = "#FFFFFF"
    pie_colors = ["#1E88E5", "#42A5F5", "#64B5F6"]

    # Set the figure style dynamically
    fig, ax = plt.subplots()
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Pie chart with customizations
    wedges, texts, autotexts = ax.pie(
        grouped_expenses,
        labels=grouped_expenses.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=pie_colors,
        wedgeprops={'edgecolor': 'black'},  # Black borders for wedges
        textprops={'color': text_color}    # Adjust text color
    )
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Update autopct text size
    for autotext in autotexts:
        autotext.set_color(text_color)
        autotext.set_fontsize(10)

    # Display in Streamlit
    st.pyplot(fig)