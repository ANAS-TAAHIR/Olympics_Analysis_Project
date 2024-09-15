from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import preprocess,helper
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff


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
        st.title('Editions')
        st.header(edition)
    
    with col2:
        st.title('Hosts')
        st.header(cities)
    
    with col3:
        st.title('Sports')
        st.header(sports)
    
    with col4:
        st.title('Events')
        st.header(events)
    
    with col5:
        st.title('Nations')
        st.header(nations)
    
    with col6:
        st.title('Athletes')
        st.header(athletes)

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

if user_menu == 'Country-wise Analysis':
    st.title('Country-wise Analysis')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    selected_country = st.selectbox('Select Country:', country)

    st.header(selected_country + ' Medal Tally over the years')
    country_medal_tally = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_medal_tally, x='Year', y='Medals')
    fig.update_traces(line=dict(color='blueviolet')) 

    st.plotly_chart(fig)

    st.header(selected_country + ' Excels in the following Sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    heatmap = sns.heatmap(pt, ax=ax, cmap='Purples_r', annot=True)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.patch.set_facecolor('none')
    st.pyplot(fig)

    st.header('Top 10 Athletes from ' + selected_country)
    athletes_df = helper.get_top_athletes_by_country(df, selected_country)
    st.table(athletes_df)

if user_menu == 'Athlete-wise Analysis':
    st.title('Athlete-wise Analysis')

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    st.header('Distribution of Age of Athletes')
    fig = ff.create_distplot([x1, x2, x3, x4], group_labels=['Overall', 'Gold', 'Silver', 'Bronze'], colors=['#D3D3D3', '#FFD700', '#C0C0C0', '#CD7F32'],show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    athlete = df['Name'].dropna().unique().tolist()
    athlete.sort()
    selected_athlete = st.selectbox('Select Athlete:', athlete)

    st.header(selected_athlete + ' Medal Tally over the Years')
    athlete_medal_tally = df[df['Name'] == selected_athlete]
    athlete_medal_tally = athlete_medal_tally.groupby(['Year', 'Medal', 'Sport','Event']).size().reset_index(name='Count')
    medal_colors = {
        'Gold': '#FFD700',  # Gold color
        'Silver': '#C0C0C0',  # Silver color
        'Bronze': '#CD7F32'  # Bronze color
    }
    fig = px.bar(athlete_medal_tally, x='Year', y='Count', color='Medal', 
                color_discrete_map=medal_colors, barmode='group')
    st.plotly_chart(fig)

    st.header(f"{selected_athlete} Participated in the Following Sports")
    sports = athlete_medal_tally['Sport'].unique().tolist()
    sports.sort()
    if sports:
        st.write('\n'.join(f"- {sport}" for sport in sports))
    else:
        st.write("No sports data available for this athlete.")

    st.header(f"{selected_athlete} Participated in the Following Events")
    events = athlete_medal_tally['Event'].unique().tolist()
    events.sort()
    if events:
        st.write('\n'.join(f"- {event}" for event in events))
    else:
        st.write("No events data available for this athlete.")


    st.header(selected_athlete + ' Medal Tally')
    medal_tally = athlete_medal_tally.groupby('Medal').size().reset_index(name='Medals')
    fig = px.pie(medal_tally, values='Medals', names='Medal', title='Medal Tally')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalists Only)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    # ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60)
    ax.set_xlabel('Weight')
    ax.set_ylabel('Height')
    ax.set_title('Scatter Plot of Weight vs Height by Medal and Sex')

    ax.legend(title='Medal and Sex')
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)