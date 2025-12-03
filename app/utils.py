import pandas as pd
import streamlit as st

def display_data_summary(df):
    """Display basic data summary in Streamlit"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        st.metric("Number of Countries", df['Country'].nunique())
    
    with col3:
        st.metric("Years Covered", f"{df['Year'].min()} - {df['Year'].max()}")
    
    # Show basic statistics
    with st.expander("Dataset Statistics"):
        st.dataframe(df.describe())
    
    # Show missing values info
    with st.expander("Missing Values Information"):
        null_counts = df.isnull().sum()
        st.dataframe(null_counts[null_counts > 0])

def create_filters(df):
    """Create interactive filters for the dashboard"""
    st.sidebar.header("📊 Filters")
    
    # Year range filter
    years = sorted(df['Year'].unique())
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years)))
    )
    
    # Region filter
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Select Region", regions)
    
    # Happiness score filter
    min_score, max_score = float(df['Happiness_Score'].min()), float(df['Happiness_Score'].max())
    score_range = st.sidebar.slider(
        "Happiness Score Range",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score)
    )
    
    # Apply filters
    filtered_df = df[
        (df['Year'] >= year_range[0]) & 
        (df['Year'] <= year_range[1]) &
        (df['Happiness_Score'] >= score_range[0]) &
        (df['Happiness_Score'] <= score_range[1])
    ]
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    return filtered_df, year_range, selected_region, score_range