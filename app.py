import streamlit as st
import pandas as pd
import plotly.express as px

# Read data
df = pd.read_csv(r'dummy_financial_data.csv')

# Set the Streamlit app title and introduction
st.title('Intelligent Dashboard')
st.write("Welcome to the Intelligent Dashboard.")
st.write("Use the filters on the left to explore financial data for different subsidiaries and time periods.")

# Initialize Session State
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Sidebar for filtering options
st.sidebar.subheader('Filter Data')
subsidiary_filter = st.sidebar.selectbox('Select Subsidiary', ['All Subsidiaries'] + list(df['Subsidiary Name'].unique()))
period_filter = st.sidebar.selectbox('Select Period', ['Yearly', 'Quarterly'])

# Filter the data based on user selections
if subsidiary_filter == 'All Subsidiaries':
    filtered_data = df.copy()
else:
    filtered_data = df[df['Subsidiary Name'] == subsidiary_filter]

# Update the period filter logic and chart labels
if period_filter == 'Quarterly':
    filtered_data['Period'] = filtered_data['Year'].astype(str) + ' Q' + filtered_data['Month'].astype(str)
    chart_title = f'{subsidiary_filter} - Quarterly Financial Data'
elif period_filter == 'Yearly':
    filtered_data['Period'] = filtered_data['Year'].astype(str)
    chart_title = f'{subsidiary_filter} - Yearly Financial Data'
else:
    filtered_data['Period'] = filtered_data['Month'].astype(str)
    chart_title = f'{subsidiary_filter} - Monthly Financial Data'

# Group the data by Year and Period
filtered_data = filtered_data.groupby(['Year', 'Period']).agg({'Revenue': 'sum', 'Expenses': 'sum', 'Profit': 'sum'}).reset_index()

st.markdown("---")

# Display the filtered data in a table
st.subheader(f'{subsidiary_filter} - Data Overview')
st.write(filtered_data)

# Export the filtered data (optional)
st.sidebar.subheader('Export Data')
if st.sidebar.button('Export Filtered Data to CSV'):
    filtered_data.to_csv('filtered_financial_data.csv', index=False)

# Function to display Summary Statistics
def display_summary_statistics(data):
    st.subheader(f'{subsidiary_filter} - Summary Statistics')
    st.write("Total Revenue:", data['Revenue'].sum())
    st.write("Total Expenses:", data['Expenses'].sum())
    st.write("Total Profit:", data['Profit'].sum())

# Function to display Trend Analysis - Line Chart
def display_trend_analysis_line(data):
    st.subheader('Trend Analysis - 1')
    trend_fig = px.line(data, x='Period', y=['Revenue', 'Expenses', 'Profit'], title=chart_title)
    st.plotly_chart(trend_fig)

# Function to display Trend Analysis - Stacked Bar Chart
def display_trend_analysis_stacked_bar(data):
    st.subheader('Trend Analysis - 2')
    stacked_bar_fig = px.bar(data, x='Period', y=['Revenue', 'Expenses', 'Profit'], barmode='relative', title=chart_title)
    st.plotly_chart(stacked_bar_fig)

st.markdown("---")

# Display Summary Statistics
display_summary_statistics(filtered_data)

st.markdown("---")

# Display Trend Analysis - Line Chart
display_trend_analysis_line(filtered_data)

st.markdown("---")

# Display Trend Analysis - Stacked Bar Chart
display_trend_analysis_stacked_bar(filtered_data)
