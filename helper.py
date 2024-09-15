import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].sort_values(by='Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Bronze'] + medal_tally['Gold'] + medal_tally['Silver'] 
    return medal_tally

def year_country_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def fetch_medal_tally(df,year, country):
    flag = 0
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if country == 'Overall' and year == 'Overall':
        temp_df = medal_df
    if country != 'Overall' and year == 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if country == 'Overall' and year != 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if country != 'Overall' and year != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
    if flag == 1:
        temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Year').reset_index()
    else:
        temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold', ascending=False).reset_index()
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']

    return temp_df

def participation_stats(df,col):
    participating_nation = df.drop_duplicates(subset=['Year', col])
    participating_nation = participating_nation['Year'].value_counts().reset_index().sort_values('Year').rename(columns={'Year':'Edition','count':col})
    return participating_nation

def most_successful_athletes(df, sports):
    temp_df = df.dropna(subset=['Medal'])
    if sports != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sports]
    temp_df = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport' ,'region']].drop_duplicates('Name')
    temp_df = temp_df.rename(columns={'count':'Medals', 'region':'Country', 'Sport':'Sports'}).reset_index(drop=True)
    return temp_df

def yearwise_medal_tally(df, country):
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    temp_df['Medals'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    return temp_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    return temp_df

def get_top_athletes_by_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    # Group by both 'Name' and 'Sport' to distinguish athletes with the same name
    athlete_medals = temp_df.groupby(['Name', 'Sport']).size().reset_index(name='Medals')
    
    # Merge with original dataframe to get the other details and avoid duplicate athletes
    result_df = athlete_medals.merge(df[['Name', 'Sport', 'region']].drop_duplicates(), on=['Name', 'Sport'])
    
    # Drop duplicates and select necessary columns
    result_df = result_df[['Name', 'Medals', 'Sport']].sort_values(by='Medals', ascending=False)
    
    # Rename columns as per the requirement
    result_df = result_df.rename(columns={'Medals': 'Medals', 'Sport': 'Sports'}).reset_index(drop=True)
    result_df = result_df.head(10)
    return result_df

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final