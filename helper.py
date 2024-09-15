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