import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(folder_path) -> pd.DataFrame:
    """
    Load and combine CSV files from subfolders (years).
    Each subfolder should represent a year and contain monthly CSV files.

    Parameters:
    folder_path (str): Path to the main folder containing budget data.

    Returns:
    pd.DataFrame: Combined dataframe containing all budget data.
    """
    all_data = []
    for year_folder in os.listdir(folder_path):
        year_path = os.path.join(folder_path, year_folder)
        if os.path.isdir(year_path):
            for file in os.listdir(year_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(year_path, file)
                    df = pd.read_csv(file_path)
                    df['anno'] = year_folder  # Add year column
                    all_data.append(df)
    # Combine all dataframes
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        # Fix data formats
        combined_df['importo'] = combined_df['importo'].str.replace(',', '.').astype(float)
        return combined_df
    else:
        return pd.DataFrame()


def preprocess_data(df) -> pd.DataFrame:
    """
    Preprocess data for analysis.

    Parameters:
    df (pd.DataFrame): Input dataframe.

    Returns:
    pd.DataFrame: Processed dataframe.
    """
    df['mese'] = pd.Categorical(
        df['mese'],
        categories=[
            'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
            'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
        ],
        ordered=True
    )
    return df


# App Layout
st.title("Personal Budget Dashboard")

# Sidebar for folder selection
folder_path = st.sidebar.text_input("Enter the path to your budget folder:")
if folder_path:
    data = load_data(folder_path)

    if not data.empty:
        data = preprocess_data(data)

        # Filters
        st.sidebar.header("Filters")
        selected_year = st.sidebar.multiselect(
            "Select Year(s):", data['anno'].unique(), default=data['anno'].unique()
        )
        selected_months = st.sidebar.multiselect(
            "Select Month(s):", data['mese'].unique(), default=data['mese'].unique()
        )
        selected_categories = st.sidebar.multiselect(
            "Select Category(s):", data['categoria'].unique(), default=data['categoria'].unique()
        )

        # Apply filters
        filtered_data = data[
            (data['anno'].isin(selected_year)) &
            (data['mese'].isin(selected_months)) &
            (data['categoria'].isin(selected_categories))
        ]

        # Display filtered data
        st.header("Filtered Data")
        st.dataframe(filtered_data)

        # Visualizations
        st.header("Visualizations")

        # Spending by Category
        st.subheader("Spending by Category")
        category_spending = filtered_data.groupby('categoria')['importo'].sum()
        fig1, ax1 = plt.subplots()
        category_spending.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_ylabel("Total Spending")
        ax1.set_title("Spending by Category")
        st.pyplot(fig1)

        # Monthly Spending Trend
        st.subheader("Monthly Spending Trend")
        monthly_spending = (
            filtered_data.groupby(['anno', 'mese'])['importo'].sum()
            .unstack(0)  # Separate years into columns
        )
        fig2, ax2 = plt.subplots()
        monthly_spending.plot(ax=ax2, marker='o')
        ax2.set_ylabel("Total Spending")
        ax2.set_title("Monthly Spending Trend")
        st.pyplot(fig2)

        # Pie Chart for Category Distribution
        st.subheader("Category Distribution")
        fig3, ax3 = plt.subplots()
        category_spending.plot.pie(ax=ax3, autopct='%1.1f%%', startangle=90)
        ax3.set_ylabel("")
        ax3.set_title("Spending by Category")
        st.pyplot(fig3)

        # Statistics
        st.header("Summary Statistics")
        st.write(f"**Total Spending:** {filtered_data['importo'].sum():.2f}")
        st.write(f"**Average Spending per Transaction:** {filtered_data['importo'].mean():.2f}")
        st.write(f"**Number of Transactions:** {filtered_data.shape[0]}")
    else:
        st.error("No data found in the specified folder.")
else:
    st.info("Please enter the folder path to load your budget data.")
