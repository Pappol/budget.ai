import streamlit as st
import pandas as pd


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