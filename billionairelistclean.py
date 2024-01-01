import csv
import pandas as pd
import numpy as np


##Clean Industry
def clean_industry_elements(x):
        if isinstance(x,str):
            x = x.replace("['", "").replace("']", "")
            x = x.replace("&#38;","and").replace("&","and")
            x = x.rstrip()
            x = "Media and Entertainment" if x =="Media" else x
            x = "Finance and Investments" if x =="Finance" else x
            x = "Telecom" if x =="Telecommunications" else x
            x = "Food and Beverage" if x =="Food" else x
            x = "Gambling and Casinos" if x =="Gambling" else x
            x = "Healthcare" if x =="Health care" or x =="Health Care" else x
        return x

def clean_blank_industry(row):
     if pd.isna(row['business_industries']) and pd.notna(row['business_category']):
          row['business_industries'] = row['business_category']
     return row['business_industries']

def clean_industry(df):

    df['business_industries'] =df.apply(clean_blank_industry,axis=1)
    
    df['business_industries'] = df['business_industries'].apply(clean_industry_elements)

    df['business_industries'] = df['business_industries'].astype('category')

    # print(df.groupby('business_industries').count().sort_values(by='business_industries',ascending=False))

    return df


##Clean Birth Year
def birth_date_blank(x):
    if pd.isna(x['birth_date']) and x['age']>0:
          x['birth_year'] =  x['year'] - x['age']-1
    elif pd.isna(x['birth_date']) and x['age']==0:
         x['birth_year'] = np.nan
    elif x['age']==0:
         x['birth_year'] = x['birth_date'].year
    else:
         x['birth_year'] = x['birth_date'].year

    return x['birth_year']


def clean_birth_year(df):
    df['birth_year'] = df.apply(birth_date_blank, axis=1)
    return df

##Clean Name

def clean_name(name):
    if isinstance(name,str):
            name = name.replace("&#38;","and").replace("&","and")
            name = name.replace("and family","").replace("and Family","")
            name = name.rstrip()
    return name


def clean_empty_birth_days(df):

    mask = df['birth_date'].notna()

    for name in df['full_name'].unique():
     if mask[df['full_name'] == name].any():
            # Get the first non-NA 'birth_date'
            dob = df.loc[mask & (df['full_name'] == name), 'birth_date'].iloc[0]
            # Set this 'birth_date' for all entries with the same 'full_name'
            df.loc[df['full_name'] == name, 'birth_date'] = dob


    return df
     

def classify_age(row):
    if pd.isna(row['age']) or row['age'] == 0:
        row['age_category'] = '-'
    elif row['age']<=20:
        row['age_category'] = '<20'
    elif row['age']<=30:
        row['age_category'] = '21-30'
    elif row['age']<=40:
        row['age_category'] = '31-40'
    elif row['age']<=50:
        row['age_category'] = '41-50'
    elif row['age']<=60:
        row['age_category'] = '51-60'
    else:
        row['age_category'] = '60+'
    
    return row['age_category']

def classify_first_time(df):
    # Ensure 'year' is sorted
    df = df.sort_values(by=['full_name', 'year'], ascending=[True, True])

    # Identify the first occurrence of each 'full_name'
    first_occurrences = df.duplicated(subset='full_name', keep='first')

    # Set 'listing_instance' to 'First' where it's the first occurrence
    df.loc[~first_occurrences, 'listing_instance'] = 'First'

    return df




if __name__ == "__main__":
    df = pd.read_csv('BillionaireList(init).csv')

    df.info()
    df['age_category'] = ['-']*len(df)
    df['listing_instance'] = ['notFirst']*len(df)

    df['full_name']=df['full_name'].apply(clean_name)
    df['first_name']=df['first_name'].apply(clean_name)
    df['last_name']=df['last_name'].apply(clean_name)
    df['organization_name']=df['organization_name'].apply(clean_name)

    df['year'] = df['year'].astype(int)
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')



    df['birth_year'] = 0

    # df.info()
    df = clean_empty_birth_days(df)
    df =  clean_industry(df)
    df = clean_birth_year(df)
    df = classify_first_time(df)
    df['age'] = df['year'] - df['birth_year']
    df['age_category'] = df.apply(classify_age,axis=1)
    

    df['UID'] = df['full_name'].astype(str) + df['birth_year'].astype(str).replace(".0","")

    df.to_csv('BillionaireListCleaned.csv',index=False)

    df_cleaned = pd.read_csv('BillionaireListCleaned.csv')


   
    print("--CLEANED--")
    value_counts = df_cleaned['year'].value_counts().to_frame()
    print(value_counts.style.background_gradient(cmap='Blues'))


"""
 things left to do:
 1. Get the unique items that have blank "Birth Years" and get ChatGPT to determine what the birth date is
 2. Get ChatGPT to determine the following
 - are they self-made or did they inherit?
 - what is their highest education background?
 - what is their country of birth?
 - What role got them to being an entrepreneur? inheritance, entrepreneurship, career, Actor, Athlete, other...?

 3. Write python to classify
 - First year they became a billionaire
    - Classify which age they first became a billionaire?
 - Mark the top 15 industries and mark "Others"
 - Mark the top 15 country_of residence, country_of_citizenzhip and mark "Others"

 4. Highlight the standouts in their industry
 - Only Oprah is the Actress / Actor who is a billionaire (verify)
 - Only Michael Jordan is the billionaire who is an athlete (verify)

 
 
"""