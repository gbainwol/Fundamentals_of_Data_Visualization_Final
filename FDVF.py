import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import streamlit as st

# Written section
written_section = """
# Interactive COVID-19 Data Visualization Page by Garrett Bainwol
6/24/2023
## LINK TO CSVs and CODE (note if you download the code and CSVs you must update the file path):
https://github.com/gbainwol/Fundamentals_of_Data_Visualization_Final

That is the link to the repository on GitHub
## Introduction:
In this project, I have developed an interactive data visualization page focusing on COVID-19 data. The data used for this project is sourced from the Johns Hopkins COVID-19 Data GitHub repository. The project utilizes two datasets: a global dataset and a specific US dataset. Both datasets provide information such as latitude, longitude, COVID-19 cases, and deaths. The global dataset includes data by country/region, while the US dataset includes data by population, state, and city/town/county. For the purpose of this project, the data has been filtered to include values from the day 03-09-2023.

The primary goal of this project is to present COVID-19 data in an engaging and informative manner. The design plays a crucial role in enhancing the user experience and facilitating the exploration of the data.note there are still some bugs like the fact the top 5 chart for Country cases only displays India, United States, and France and also the fact that the ratios for States and City/Town/County prints twice. I spent hours toying around trying to get various elements to work but atlas there are still some bugs.Streamlit did not want to work with the most current version of altair. I also used folium to create the heatmaps.

## Key Elements of the Page:
The interactive COVID-19 data visualization page incorporates several key elements that contribute to its effectiveness:

1. Diverse Ratio Data: The page presents various ratio calculations, including cases per population, deaths per population, and deaths-to-cases ratio. These ratios provide insights into the severity of the COVID-19 situation in different regions.

2. Interactive Bar Chart: The page features an interactive bar chart showcasing the top countries or regions based on COVID-19 cases or deaths. Users can choose the number of countries to display and the metric (cases or deaths) for the chart. This bar chart allows users to compare the COVID-19 impact across different countries or regions.

3. Interactive Heatmaps: Both the global and US datasets are visualized through interactive heatmaps. The heatmaps provide a geographical representation of COVID-19 cases, allowing users to identify hotspots and patterns. Users can toggle between global and US data and choose the metric (cases or deaths) for the heatmap.

4. Interactive Scatterplot: For the US data, the page includes an interactive scatterplot that depicts the relationship between COVID-19 cases and deaths. Users can explore the scatterplot for a specific state or city/town/county, visualizing the data points based on population size. This scatterplot facilitates the examination of COVID-19 trends and potential correlations.

5. Useful Info and Statistics: The page also provides useful information and statistics, including total COVID-19 cases and deaths for a selected country/region or state. Additionally, ratio tables offer insights into the impact of COVID-19 on different areas, highlighting key metrics such as cases per population and deaths per population.

6. Interactive Pie Chart: 
The interactive COVID-19 data visualization page includes two pie charts that provide insights into the distribution of COVID-19 cases and deaths across the 50 states of the United States. Each pie chart represents a different aspect of the data.

The first pie chart showcases the distribution of COVID-19 cases among the 50 states. It visualizes the proportion of cases attributed to each state, allowing users to quickly identify the states with the highest number of cases and compare them to the states with lower case counts. The size of each slice in the pie chart corresponds to the relative number of cases in a specific state.

The second pie chart focuses on the distribution of COVID-19 deaths across the 50 states. It presents the proportion of deaths attributed to each state, offering a visual representation of the impact of the virus in different parts of the country. By examining the relative sizes of the slices in the pie chart, users can gain an understanding of the states with the highest mortality rates and identify any disparities.

Both pie charts provide a clear visual summary of the COVID-19 situation across the 50 states, allowing users to grasp the relative magnitude of cases and deaths in each state. This information can help users identify regions that may require more attention or resources in combating the virus. The interactivity of the page may also allow users to select specific states or filter the data based on different criteria, further enhancing the exploration and analysis of the COVID-19 impact at the state level.
## Evaluation Approach:
The evaluation approach for this project focused on creating dynamic, organized tables, and charts that deliver visually pleasing yet informative data. The page offers flexibility by allowing users to select their desired data type (global or US) and choose the specific state or city/town/county for analysis. The interactive nature of the visualizations promotes engagement and empowers users to explore the data according to their preferences.

Throughout the development process, I encountered various challenges. The integration of different libraries and the management of dependencies required significant effort and troubleshooting. Despite the difficulties faced, I dedicated considerable time to ensuring a seamless user experience and resolving errors to deliver a functional and visually appealing data visualization page.The goal was to make the page intersting to use and interactive.

## Findings and Future Improvements:
The project successfully achieved the goal of providing an interactive COVID-19 data visualization experience. The ratio calculations and interactive visualizations allowed users to gain insights into the severity and impact of the pandemic. The dynamic nature of the page allowed for customized exploration and analysis of the data.

However, the development process revealed the complexity of integrating different libraries and managing dependencies. Debugging and resolving errors took a considerable amount of time and effort. In the future, I would approach the project with a deeper understanding of library compatibility and version management to streamline the development process.

Overall, this project serves as a testament to the challenges faced during the creation of interactive data visualization pages. The combination of design, data analysis, and coding expertise required considerable dedication and perseverance to deliver an engaging and informative end product.
"""

# Display written section
st.markdown(written_section)
st.header(" Data Visualizations below")

#change file path for global_data and us_data to run code 

st.header(' Global Visualizations')
# Load data
global_data = pd.read_csv("/Users/garrettbainwol/Desktop/global2.csv")
us_data = pd.read_csv("/Users/garrettbainwol/Desktop/us2.csv")

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
