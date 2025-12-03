import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def create_univariate_plots(df):
    """Create univariate visualizations"""
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Happiness_Score'], kde=True, color='skyblue', bins=30, ax=ax1)
    ax1.set_title('Distribution of Happiness Scores')
    ax1.set_xlabel('Happiness Score')
    ax1.set_ylabel('Frequency')
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=df['GDP_Per_Capita'], color='lightgreen', ax=ax2)
    ax2.set_title('Boxplot of Log GDP Per Capita')
    ax2.set_xlabel('Log GDP Per Capita')
    
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    region_counts = df['Region'].value_counts()
    sns.barplot(x=region_counts.values, y=region_counts.index, palette='viridis', ax=ax3)
    ax3.set_title('Number of Observations per Region')
    ax3.set_xlabel('Count')
    ax3.set_ylabel('Region')
    
    return fig1, fig2, fig3

def create_bivariate_plots(df):
    """Create bivariate visualizations"""
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='GDP_Per_Capita', y='Happiness_Score', alpha=0.6, ax=ax1)
    ax1.set_title('Happiness Score vs. GDP Per Capita')
    ax1.set_xlabel('Log GDP Per Capita')
    ax1.set_ylabel('Happiness Score')
    
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    sns.boxplot(x='Happiness_Score', y='Region', data=df, palette='Set2', ax=ax2)
    ax2.set_title('Happiness Score Distribution by Region')
    ax2.set_xlabel('Happiness Score')
    ax2.set_ylabel('Region')
    
    # Correlation heatmap
    corr_cols = ['Happiness_Score', 'GDP_Per_Capita', 'Social Support', 
                 'Life_Expectancy', 'Freedom', 'Generosity', 'Corruption']
    correlation = df[corr_cols].corr()
    
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", 
                linewidths=0.5, ax=ax3, square=True)
    ax3.set_title('Correlation Heatmap of Key Variables')
    
    return fig1, fig2, fig3

def create_interactive_plot(df):
    """Create interactive multi-dimensional plot"""
    fig = px.scatter(
        df,
        x="GDP_Per_Capita",
        y="Happiness_Score",
        color="Region",
        size="Life_Expectancy",
        hover_name="Country",
        animation_frame="Year",
        title="Interactive: GDP vs Happiness (Bubble Size = Life Expectancy)",
        template="plotly_white",
        hover_data=['Social Support', 'Freedom', 'Generosity']
    )
    
    # Fix ranges for better animation
    fig.update_layout(
        xaxis_range=[5.5, 12],
        yaxis_range=[2, 9],
        height=600
    )
    
    return fig

def create_geospatial_map(df, year=None):
    """Create choropleth map for happiness scores"""
    if year:
        df_map = df[df['Year'] == year]
        title = f"Global Happiness Scores ({year})"
    else:
        df_map = df
        title = "Global Happiness Scores (All Years)"
    
    fig = px.choropleth(
        df_map,
        locations="Country",
        locationmode="country names",
        color="Happiness_Score",
        hover_name="Country",
        hover_data=['Region', 'GDP_Per_Capita', 'Life_Expectancy'],
        color_continuous_scale=px.colors.sequential.Viridis,
        title=title,
        height=600
    )
    
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
    
    return fig

def create_time_series(df):
    """Create time series plot of average happiness"""
    yearly_avg = df.groupby('Year')['Happiness_Score'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=yearly_avg, x='Year', y='Happiness_Score', 
                 marker='o', color='purple', ax=ax)
    ax.set_title('Global Average Happiness Score Trend (2005-2023)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Happiness Score')
    ax.grid(True)
    
    return fig

def create_top_countries_chart(df, year, n=10):
    """Create bar chart of top N happiest countries"""
    df_year = df[df['Year'] == year]
    top_n = df_year.nlargest(n, 'Happiness_Score')
    
    fig = px.bar(
        top_n,
        x='Happiness_Score',
        y='Country',
        orientation='h',
        color='Happiness_Score',
        color_continuous_scale='viridis',
        title=f'Top {n} Happiest Countries ({year})',
        hover_data=['Region', 'GDP_Per_Capita', 'Life_Expectancy'],
        height=500
    )
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig