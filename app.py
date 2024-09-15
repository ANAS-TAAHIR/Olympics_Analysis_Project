from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import preprocess,helper
import plotly.express as px
import seaborn as sns

st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio('Select Analysis:', ['Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis'])

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocess.preprocess(df, region_df)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, country = helper.year_country_list(df)
    selected_year = st.sidebar.selectbox('Select Year:', years)
    selected_country = st.sidebar.selectbox('Select Country:', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Medal Tally')
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title(selected_country + ' Overall Medal Tally')
    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title('Overall Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(selected_country + ' Medal Tally in ' + str(selected_year) + ' Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    edition = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    st.title('Olympics Top Statistics')

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)


    with col1:
        st.header('Editions')
        st.title(edition)
    
    with col2:
        st.header('Hosts')
        st.title(cities)
    
    with col3:
        st.header('Sports')
        st.title(sports)
    
    with col4:
        st.header('Events')
        st.title(events)
    
    with col5:
        st.header('Nations')
        st.title(nations)
    
    with col6:
        st.header('Athletes')
        st.title(athletes)

    st.title('Nations Participitaion by Edition')
    no_participating_nation = helper.participation_stats(df,'region')
    fig = px.line(no_participating_nation, x='Edition', y='region')
    fig.update_traces(line=dict(color='red')) 
    st.plotly_chart(fig)

    st.title('Events held by Edition')
    event_participating_nation = helper.participation_stats(df,'Event')
    fig = px.line(event_participating_nation, x='Edition', y='Event')
    fig.update_traces(line=dict(color='#00FF00')) 
    st.plotly_chart(fig)

    st.title('Athletes Participitaion by Edition')
    athlete_participating_nation = helper.participation_stats(df,'Name')
    fig = px.line(athlete_participating_nation, x='Edition', y='Name')
    fig.update_traces(line=dict(color='#FFD700')) 
    st.plotly_chart(fig)

    st.title('No. of Events by Sports in each Edition')
    events_sports = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
    fig, ax = plt.subplots(figsize=(20, 20))
    heatmap = sns.heatmap(
    events_sports.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
    ax=ax,
    annot=True,
    fmt='d',
    cmap='Purples_r', # Adjust colormap as needed
    vmin = 50,
    vmax = 0,
    cbar_kws={'label': 'Number of Events'})

    # Set the color of the tick labels (index and year columns) to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.patch.set_facecolor('none')  # Set the background color of the Figure to black

    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sports:', sports_list)

    successful_athletes = helper.most_successful_athletes(df, selected_sport)
    st.table(successful_athletes)