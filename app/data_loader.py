import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    """Load and preprocess the World Happiness Report dataset"""
    try:
        # Adjust path according to your structure
        df = pd.read_csv('data/World Happiness Report.csv')
        
        # Fill missing numeric values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        # Rename columns for easier access
        df.rename(columns={
            'Country Name': 'Country',
            'Regional Indicator': 'Region',
            'Life Ladder': 'Happiness_Score',
            'Log GDP Per Capita': 'GDP_Per_Capita',
            'Healthy Life Expectancy At Birth': 'Life_Expectancy',
            'Freedom To Make Life Choices': 'Freedom',
            'Perceptions Of Corruption': 'Corruption'
        }, inplace=True)
        
        # Convert Region column to string and handle NaN values
        if 'Region' in df.columns:
            df['Region'] = df['Region'].astype(str).replace('nan', 'Unknown')
        
        # Convert other string columns to proper strings
        if 'Country' in df.columns:
            df['Country'] = df['Country'].astype(str)
        
        return df
    
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'World Happiness Report.csv' is in the data/ folder")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def get_most_recent_data(df):
    """Get data for the most recent year"""
    most_recent_year = df['Year'].max()
    return df[df['Year'] == most_recent_year]

def get_yearly_average(df):
    """Calculate yearly average happiness scores"""
    return df.groupby('Year')['Happiness_Score'].mean().reset_index()