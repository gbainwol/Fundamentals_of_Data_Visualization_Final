import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import streamlit as st

st.header(' Global Visualizations')
# Load data
# replace the values for filepath_1 and filepath_2 with the correct path 
filepath_1= "/global2.CSV"
filepath_2= "/us2.CSV"
global_data = pd.read_csv(filepath_1)
us_data = pd.read_csv(filepath_2)

def compute_ratios(df):
    df['Cases/Population'] = df['cases'] / df['Population']
    df['Deaths/Population'] = df['deaths'] / df['Population']
    df['Deaths/Cases'] = df['deaths'] / df['cases']
    # Replace infinite values with np.nan
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df

if __name__ == '__main__':
    st.sidebar.header('Global Options')
    country = st.sidebar.selectbox('Pick Country for Case Numbers and Deaths', global_data['Country/Region'].unique())
    bar_chart_metric = st.sidebar.radio('Select Metric for Bar Chart', ('cases', 'deaths'))
    num_countries_choice = st.sidebar.selectbox('Number of Countries for Bar Chart', ('Top 5', 'Top 10', 'Top 25'))

    if num_countries_choice == 'Top 5':
        num_countries = 5
    elif num_countries_choice == 'Top 10':
        num_countries = 10
    else:
        num_countries = 25

    # Global Data - Country Stats
    global_data_country = global_data[global_data['Country/Region'] == country][['Country/Region', 'cases', 'deaths']]
    global_data_country['Deaths/Cases Ratio'] = global_data_country['deaths'] / global_data_country['cases']
    global_data_country.columns = ['Country', 'Total Covid-19 Cases', 'Total Covid-19 Deaths', 'Deaths/Cases Ratio']

    st.header( f"COVID-19 Total Cases and Deaths in {country}")
    st.table(global_data_country)

    # Bar Chart - Total Cases by Country
    global_data_sorted = global_data.nlargest(num_countries, bar_chart_metric)
    bar_chart = alt.Chart(global_data_sorted).mark_bar().encode(
        x=alt.X(f"{bar_chart_metric}:Q", axis=alt.Axis(title=bar_chart_metric.title())),
        y=alt.Y('Country/Region:N', sort='-x'),
        color='Country/Region:N',
        tooltip=['Country/Region', bar_chart_metric]
    ).properties(title=f"Top {num_countries} Countries by {bar_chart_metric.title()}",
                width=600,
                height=400)

    st.header(f"COVID-19 {bar_chart_metric.title()} by Country")
    st.altair_chart(bar_chart, use_container_width=True)

    # Heatmap of Global Data
    st.header('Global Heatmap of Cases')
    global_map = folium.Map(location=[0, 0], zoom_start=2)
    HeatMap(zip(global_data['Lat'], global_data['Long'], global_data[bar_chart_metric])).add_to(global_map)
    # Adding circles to Global Heatmap
    for _, row in global_data.iterrows():
        folium.CircleMarker(
            location=[row['Lat'], row['Long']],
            radius=5,
            fill=True,
            tooltip=f"Country: {row['Country/Region']}<br>Cases: {row['cases']}<br>Deaths: {row['deaths']}"
        ).add_to(global_map)
    folium_static(global_map)

    st.sidebar.header('US Options')

    data_type = st.sidebar.selectbox('Select Data Type', ('States', 'City/Town/County'))

    if data_type == 'States':
        state = st.sidebar.selectbox('Pick State for Scatter Graph and Ratio Info', us_data['State'].unique())
        us_data_filtered = us_data[us_data['State'] == state]
        us_data_filtered_state = us_data_filtered.groupby('State').agg({
            'Population': 'sum',
            'cases': 'sum',
            'deaths': 'sum'
        }).reset_index()
        us_data_filtered_state = compute_ratios(us_data_filtered_state)
        st.header('US Visualizations and Tables')
        
        st.header(f"Ratios for {state}")
        st.table(us_data_filtered_state[['State', 'Cases/Population', 'Deaths/Population', 'Deaths/Cases']])

        # Scatter Plot for selected state
        scatter_chart = alt.Chart(us_data_filtered).mark_circle().encode(
            alt.X('cases', scale=alt.Scale(zero=False)),
            alt.Y('deaths', scale=alt.Scale(zero=False, padding=1)),
            size='Population',
            color='State',
            tooltip=['State', 'cases', 'deaths', 'Population']
        ).interactive()

        st.header(f"COVID-19 Cases vs Deaths in {state}")
        st.altair_chart(scatter_chart, use_container_width=True)
    else:
        city_town_county = st.sidebar.selectbox('Pick City/Town/County for Ratio Info', us_data['City/Town/County'].unique())
        us_data_filtered_city = us_data[us_data['City/Town/County'] == city_town_county]
        us_data_filtered_city = compute_ratios(us_data_filtered_city)

        st.header(f"Ratios for {city_town_county}")
        st.table(us_data_filtered_city[['City/Town/County', 'Cases/Population', 'Deaths/Population', 'Deaths/Cases']])

    # State-Level Pie Charts for Deaths and Cases
    us_data_total = us_data.groupby('State').agg({
        'Population': 'sum',
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index()

    total_cases = us_data_total['cases'].sum()
    total_deaths = us_data_total['deaths'].sum()

    us_data_total['Percentage Cases'] = us_data_total['cases'] / total_cases
    us_data_total['Percentage Deaths'] = us_data_total['deaths'] / total_deaths

    pie_chart_cases = alt.Chart(us_data_total).mark_arc(
        innerRadius=50
    ).encode(
        theta='Percentage Cases:Q',
        color='State:N',
        tooltip=['State', 'Population', 'cases', 'deaths']
    ).properties(
        title='US Cases by State',
        width=400,
        height=400
    )

    pie_chart_deaths = alt.Chart(us_data_total).mark_arc(
        innerRadius=50
    ).encode(
        theta='Percentage Deaths:Q',
        color='State:N',
        tooltip=['State', 'Population', 'cases', 'deaths']
    ).properties(
        title='US Deaths by State',
        width=400,
        height=400
    )

    st.header("US Cases and Deaths by State")
    st.altair_chart(pie_chart_cases | pie_chart_deaths, use_container_width=True)

    if data_type == 'States':
        state_ratios = us_data_filtered_state[['State', 'Cases/Population', 'Deaths/Population', 'Deaths/Cases']]
        state_ratios.columns = ['State', 'Cases/Population', 'Deaths/Population', 'Deaths/Cases']
        st.header(f"Ratios for {state}")
        st.table(state_ratios)
    else:
        city_town_county_ratios = us_data_filtered_city[['City/Town/County', 'Cases/Population', 'Deaths/Population', 'Deaths/Cases']]
        city_town_county_ratios.columns = ['City/Town/County', 'Cases/Population', 'Deaths/Population', 'Deaths/Cases']
        st.header(f"Ratios for {city_town_county}")
        st.table(city_town_county_ratios)

    if data_type == 'States':
        st.header(f'US Heatmap of Cases in {state}')
        us_map = folium.Map(location=[39.50, -98.35], zoom_start=4)
        us_data_state = us_data[us_data['State'] == state]
        HeatMap(zip(us_data_state['Lat'], us_data_state['Long'], us_data_state['cases'])).add_to(us_map)
        # Adding circles to US Heatmap
        for _, row in us_data_state.iterrows():
            folium.CircleMarker(
                location=[row['Lat'], row['Long']],
                radius=5,
                fill=True,
                tooltip=f"City/Town/County: {row['City/Town/County']}<br>Population: {row['Population']}<br>Cases: {row['cases']}<br>Deaths: {row['deaths']}"
            ).add_to(us_map)
        folium_static(us_map)
