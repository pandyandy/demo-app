import streamlit as st
import pandas as pd
import plotly.express as px
from keboola_streamlit import KeboolaStreamlit

st.set_page_config(layout="wide")

STORAGE_API_TOKEN = st.secrets['STORAGE_API_TOKEN']
KEBOOLA_HOSTNAME = st.secrets['KEBOOLA_HOSTNAME']

#keboola = KeboolaStreamlit(KEBOOLA_HOSTNAME, STORAGE_API_TOKEN)

# Load data
#@st.cache_data
#def get_dataframe(table_name):
#    df = keboola.get_table(table_name)
#    return df

#gdp_data = get_dataframe('in.c-data.gdp_data')
#population_data = get_dataframe("in.c-data.population_data")

gdp_data = pd.read_csv('data/gdp_data.csv')
population_data = pd.read_csv('data/population_data.csv')

gdp_data = gdp_data.sort_values(by=['Country_Name', 'Year'])
population_data = population_data.sort_values(by=['Country_Name', 'Year'])

# Merge GDP and Population data
merged_data = pd.merge(gdp_data, population_data, on=['Country_Name', 'Year'])

# Calculate GDP per Capita
merged_data['GDP_per_capita'] = merged_data['GDP'] / merged_data['Population']

# Title
st.title('🇨🇿 & friends 💰👥📊')

# Filters
col1, col2 = st.columns(2)
selected_data_type = col1.selectbox('Select data to visualize', ['GDP', 'Population', 'GDP per Capita'])

eu_countries = ["Czechia", "Austria", "Slovak Republic", "Germany", "Poland"]
selected_countries = col2.multiselect('Select countries to visualize', eu_countries, default=eu_countries)

# Select data based on user selection
filtered_data = merged_data[merged_data["Country_Name"].isin(selected_countries)]

# Define y-axis label and titles based on selection
data_type_map = {
    'GDP': ('GDP', 'GDP of EU Countries from 1990 onwards', 'GDP of EU Countries in '),
    'Population': ('Population', 'Population of EU Countries from 1990 onwards', 'Population of EU Countries in '),
    'GDP per Capita': ('GDP_per_capita', 'GDP per Capita of EU Countries from 1990 onwards', 'GDP per Capita of EU Countries in ')
}

y_axis_label, line_chart_title, bar_chart_title_prefix = data_type_map[selected_data_type]
bar_chart_title = f'{bar_chart_title_prefix}{filtered_data["Year"].max()}'

# Create plots
def create_line_chart(data, y, title):
    fig = px.line(data, x='Year', y=y, color='Country_Name', 
                  title=title,
                  labels={y: y, 'Year': 'Year', 'Country_Name': 'Country'})
    return fig

def create_bar_chart(data, y, title):
    latest_year = data['Year'].max()
    latest_data = data[data['Year'] == latest_year]
    fig = px.bar(latest_data, x=y, y='Country_Name', color='Country_Name',
                 orientation='h', 
                 title=title,
                 labels={y: y, 'Country_Name': 'Country'})
    return fig

col1.plotly_chart(create_line_chart(filtered_data, y_axis_label, line_chart_title), use_container_width=True)
col2.plotly_chart(create_bar_chart(filtered_data, y_axis_label, bar_chart_title), use_container_width=True)
