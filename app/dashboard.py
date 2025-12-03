import streamlit as st
import pandas as pd
import plotly.express as px  # Add this import
from data_loader import load_data, get_most_recent_data, get_yearly_average
from visualizations import (
    create_univariate_plots, create_bivariate_plots, 
    create_interactive_plot, create_geospatial_map,
    create_time_series, create_top_countries_chart
)
from utils import display_data_summary, create_filters

# Page configuration
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #264653;
        border-bottom: 3px solid #2A9D8F;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2A9D8F;
    }
    .stPlotlyChart {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title and description
    st.markdown('<h1 class="main-header">🌍 World Happiness Report Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("""
    Interactive visualization and analysis of global happiness data from 2005 to 2023.
    Explore relationships between happiness scores, economic indicators, and social factors.
    """)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Create filters in sidebar
    filtered_df, year_range, selected_region, score_range = create_filters(df)
    
    # Display filters summary
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Current Filters")
        st.info(f"""
        **Years:** {year_range[0]} - {year_range[1]}
        **Region:** {selected_region}
        **Happiness Score:** {score_range[0]:.2f} - {score_range[1]:.2f}
        **Filtered Records:** {len(filtered_df):,}
        """)
    
    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", 
        "📊 Basic Analysis", 
        "🎯 Interactive", 
        "🗺️ Geospatial", 
        "📋 Data"
    ])
    
    with tab1:  # Overview Tab
        st.markdown('<h2 class="section-header">📈 Dashboard Overview</h2>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                avg_happiness = filtered_df['Happiness_Score'].mean()
                st.metric("Average Happiness", f"{avg_happiness:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                avg_gdp = filtered_df['GDP_Per_Capita'].mean()
                st.metric("Avg GDP Per Capita", f"{avg_gdp:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                avg_life_exp = filtered_df['Life_Expectancy'].mean()
                st.metric("Avg Life Expectancy", f"{avg_life_exp:.1f}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                countries = filtered_df['Country'].nunique()
                st.metric("Countries", countries)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Top countries and time series in columns
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 🏆 Top 10 Happiest Countries")
            year_select = st.selectbox(
                "Select Year for Ranking",
                sorted(filtered_df['Year'].unique(), reverse=True),
                key="top_year_select"
            )
            top_chart = create_top_countries_chart(filtered_df, year_select)
            st.plotly_chart(top_chart, use_container_width=True)
        
        with col_right:
            st.markdown("#### 📈 Happiness Trend Over Time")
            trend_fig = create_time_series(filtered_df)
            st.pyplot(trend_fig)
    
    with tab2:  # Basic Analysis Tab
        st.markdown('<h2 class="section-header">📊 Univariate & Bivariate Analysis</h2>', unsafe_allow_html=True)
        
        analysis_type = st.radio(
            "Select Analysis Type",
            ["Univariate", "Bivariate"],
            horizontal=True
        )
        
        if analysis_type == "Univariate":
            st.markdown("### Distribution Analysis")
            fig1, fig2, fig3 = create_univariate_plots(filtered_df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(fig1)
            with col2:
                st.pyplot(fig2)
            
            st.pyplot(fig3)
            
            with st.expander("📝 Interpretation"):
                st.markdown("""
                **Key Insights:**
                1. Happiness scores follow a roughly normal distribution
                2. GDP per capita shows variation across countries
                3. Regional distribution shows varying data density
                """)
        
        else:  # Bivariate
            st.markdown("### Relationship Analysis")
            fig1, fig2, fig3 = create_bivariate_plots(filtered_df)
            
            st.pyplot(fig1)
            
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(fig2)
            with col2:
                st.pyplot(fig3)
            
            with st.expander("📝 Interpretation"):
                st.markdown("""
                **Key Insights:**
                1. Strong positive correlation between GDP and Happiness
                2. Regional differences in happiness distributions
                3. Social support and life expectancy highly correlated with happiness
                """)
    
    with tab3:  # Interactive Tab
        st.markdown('<h2 class="section-header">🎯 Interactive Multi-dimensional Analysis</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Interactive Bubble Chart:** Explore the relationship between GDP, Happiness, and Life Expectancy.
        Use the year slider to see changes over time. Hover over points for detailed information.
        """)
        
        # Add customization options
        col1, col2 = st.columns(2)
        with col1:
            size_by = st.selectbox(
                "Bubble Size Represents",
                ['Life_Expectancy', 'Social Support', 'Freedom', 'Generosity'],
                key="size_var"
            )
        
        with col2:
            color_by = st.selectbox(
                "Color By",
                ['Region', 'Happiness_Score', 'GDP_Per_Capita'],
                key="color_var"
            )
        
        # Create interactive plot with customizations
        fig = px.scatter(
            filtered_df,
            x="GDP_Per_Capita",
            y="Happiness_Score",
            color=color_by,
            size=size_by,
            hover_name="Country",
            animation_frame="Year",
            title=f"Interactive Analysis: {color_by} vs GDP & Happiness",
            template="plotly_white",
            hover_data=['Region', 'Life_Expectancy', 'Freedom']
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("🎮 How to Use This Visualization"):
            st.markdown("""
            - **Play Animation:** Click the play button to see changes over years
            - **Hover:** Hover over any bubble to see country details
            - **Zoom:** Use your mouse to zoom in/out
            - **Pan:** Click and drag to move around
            - **Reset:** Double-click to reset the view
            """)
    
    with tab4:  # Geospatial Tab
        st.markdown('<h2 class="section-header">🗺️ Geospatial Analysis</h2>', unsafe_allow_html=True)
        
        map_year = st.selectbox(
            "Select Year for Map",
            sorted(filtered_df['Year'].unique(), reverse=True),
            key="map_year"
        )
        
        # Create map for selected year
        map_fig = create_geospatial_map(filtered_df, map_year)
        st.plotly_chart(map_fig, use_container_width=True)
        
        # Regional analysis
        st.markdown("### Regional Analysis")
        region_data = filtered_df.groupby('Region')['Happiness_Score'].agg(['mean', 'std', 'count']).round(3)
        region_data.columns = ['Average Happiness', 'Standard Deviation', 'Country Count']
        st.dataframe(region_data.sort_values('Average Happiness', ascending=False))
        
        with st.expander("🌍 Regional Insights"):
            st.markdown("""
            **Observations:**
            - Western Europe and North America consistently show highest happiness scores
            - Sub-Saharan Africa shows more variability
            - Regional patterns remain relatively stable over time
            """)
    
    with tab5:  # Data Tab
        st.markdown('<h2 class="section-header">📋 Data Exploration</h2>', unsafe_allow_html=True)
        
        # Display data summary
        display_data_summary(filtered_df)
        
        # Data table with filters
        st.markdown("### Filtered Data Table")
        
        # Column selection
        columns = st.multiselect(
            "Select columns to display",
            filtered_df.columns.tolist(),
            default=['Country', 'Year', 'Region', 'Happiness_Score', 'GDP_Per_Capita']
        )
        
        if columns:
            # Sort options
            sort_by = st.selectbox("Sort by", columns)
            sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)
            
            # Display data
            display_df = filtered_df[columns]
            display_df = display_df.sort_values(
                sort_by, 
                ascending=(sort_order == "Ascending")
            )
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"happiness_data_filtered_{year_range[0]}_{year_range[1]}.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>World Happiness Report Dashboard | Data Source: World Happiness Report 2005-2023</p>
        <p>Created for Advanced Data Visualization Assignment</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()