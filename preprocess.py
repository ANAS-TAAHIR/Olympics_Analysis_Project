import pandas as pd

def preprocess(df, region_df):
    # filter season summer
    df = df[df['Season'] == 'Summer']
    # merge region_df
    df = df.merge(region_df, how='left', on='NOC')
    # drop duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    df['Gold'] = df['Gold'].apply(lambda x: 1 if x == True else 0)
    df['Silver'] = df['Silver'].apply(lambda x: 1 if x == True else 0)
    df['Bronze'] = df['Bronze'].apply(lambda x: 1 if x == True else 0)
    
    return df