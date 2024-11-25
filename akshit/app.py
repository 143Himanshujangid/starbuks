import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Starbucks Location Analysis", layout="wide")

# Load and prepare data
@st.cache_data
def load_data():
    # In real application, you would load from CSV
    df = pd.read_csv("https://raw.githubusercontent.com/143Himanshujangid/starbuks/main/akshit/Starbucks%20Store%20Locations.csv", encoding='latin1')
    return df

def main():
    st.title("🏪 Starbucks Store Location Analysis Dashboard")
    st.write("Analysis of Starbucks store locations across different regions")
    
    df = load_data()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Add questions dropdown in sidebar
    questions = [
        "Select a Question",
        "1. What is the geographical distribution of stores by city?",
        "2. Which cities have the highest number of stores?",
        "3. What is the distribution of ownership types?",
        "4. How are stores distributed across timezones?",
        "5. What is the average latitude/longitude by country?",
        "6. Which countries have the most locations?",
        "7. What is the distribution across states/provinces?",
        "8. What are common patterns in store naming?",
        "9. What percentage of stores have phone numbers?",
        "10. How many stores are in shopping malls?",
        "11. What is the store density in urban areas?",
        "12. Are there store clusters in neighborhoods?",
        "13. Which areas show growth potential?",
        "14. What's the average distance between stores?",
        "15. How many stores are in airports?",
        "16. What is the distribution by postcode?",
        "17. Are there patterns in store numbers?",
        "18. How many stores are in educational institutions?",
        "19. Store correlation with population density",
        "20. Commercial vs residential location split"
    ]
    
    selected_question = st.sidebar.selectbox("Analysis Questions", questions)
    
    analysis_type = st.sidebar.radio(
        "Select Analysis Type",
        ["Overview", "Store Distribution", "Ownership Analysis", "Location Analysis"]
    )
    
    if analysis_type == "Overview":
        show_overview(df)
    elif analysis_type == "Store Distribution":
        show_store_distribution(df)
    elif analysis_type == "Ownership Analysis":
        show_ownership_analysis(df)
    elif analysis_type == "Location Analysis":
        show_location_analysis(df)
    
    # Show analysis based on selected question
    if selected_question != "Select a Question":
        show_question_analysis(df, selected_question)

def show_question_analysis(df, question):
    st.header("Question Analysis")
    st.subheader(question)
    
    if "1." in question:  # Geographical distribution
        city_counts = df['City'].value_counts().head(15)
        fig = px.bar(
            x=city_counts.index,
            y=city_counts.values,
            title="Store Distribution by City",
            labels={'x': 'City', 'y': 'Number of Stores'}
        )
        st.plotly_chart(fig)
        
    elif "2." in question:  # Cities with most stores
        city_counts = df['City'].value_counts().head(10)
        fig = px.pie(
            values=city_counts.values,
            names=city_counts.index,
            title="Top 10 Cities by Store Count"
        )
        st.plotly_chart(fig)
        
    elif "3." in question:  # Ownership types
        ownership_counts = df['Ownership Type'].value_counts()
        fig = px.pie(
            values=ownership_counts.values,
            names=ownership_counts.index,
            title="Distribution of Store Ownership Types"
        )
        st.plotly_chart(fig)
        
    elif "4." in question:  # Timezone distribution
        timezone_counts = df['Timezone'].value_counts()
        fig = px.bar(
            x=timezone_counts.index,
            y=timezone_counts.values,
            title="Store Distribution by Timezone",
            labels={'x': 'Timezone', 'y': 'Number of Stores'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig)
        
    # Add more visualizations for other questions...

def show_overview(df):
    st.header("Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Stores", len(df))
    with col2:
        st.metric("Total Countries", df['Country'].nunique())
    with col3:
        st.metric("Total Cities", df['City'].nunique())
    
    # Top 10 cities by store count
    st.subheader("Top 10 Cities by Number of Stores")
    city_counts = df['City'].value_counts().head(10)
    fig = px.bar(
        x=city_counts.index,
        y=city_counts.values,
        labels={'x': 'City', 'y': 'Number of Stores'}
    )
    st.plotly_chart(fig)

def show_store_distribution(df):
    st.header("Store Distribution Analysis")
    
    # Store distribution by timezone
    timezone_counts = df['Timezone'].value_counts().head(10)
    fig = px.bar(
        x=timezone_counts.index,
        y=timezone_counts.values,
        title="Store Distribution by Timezone",
        labels={'x': 'Timezone', 'y': 'Number of Stores'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)
    
    # Store distribution by city
    city_counts = df['City'].value_counts().head(15)
    fig = px.bar(
        x=city_counts.index,
        y=city_counts.values,
        title="Store Distribution by City",
        labels={'x': 'City', 'y': 'Number of Stores'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

def show_ownership_analysis(df):
    st.header("Ownership Type Analysis")
    
    # Ownership type distribution
    ownership_counts = df['Ownership Type'].value_counts()
    fig = px.pie(
        values=ownership_counts.values,
        names=ownership_counts.index,
        title="Distribution of Store Ownership Types"
    )
    st.plotly_chart(fig)
    
    # Ownership type by city
    ownership_by_city = df.groupby(['City', 'Ownership Type']).size().unstack(fill_value=0)
    fig = px.bar(
        ownership_by_city,
        title="Ownership Types by City",
        barmode='group'
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

def show_location_analysis(df):
    st.header("Location Analysis")
    
    # Create a scatter plot of store locations
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Store Name",
        hover_data=["City", "Country"],
        zoom=3,
        height=300,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
    # Store count by country
    country_counts = df['Country'].value_counts()
    fig = px.pie(
        values=country_counts.values,
        names=country_counts.index,
        title="Store Distribution by Country"
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
