import wikipediaapi
import csv
import pandas as pd
import numpy as np
import os
import time


def write_to_csv(df,file_name):

    #append dataframe to file without header
    with open(file_name,'a',newline='') as file:
        df.to_csv(file,mode='a',header=False,index=False)


def enrich_csv(df,write_file):
    
    file_name = write_file
    headers = list(df.columns) + ['ca_updated', 'el_updated', 'early_life', 'career']
    file_exists = os.path.exists(file_name)

    #write headers for the first time
    if not file_exists:
        with open(file_name,'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    
    if file_exists:
        check_df = pd.read_csv(file_name, dtype={'UID': str})

        # print('checkdf complete')
        print(check_df["full_name"].head(10))
        # print(f'CHECK {check_df["full_name"]}')


    if file_exists:
        print(f'Existing DATAFRAME===> {len(df)}')
        filtered_df = df[~df['UID'].isin(check_df['UID'])]
        print(f'NEW DATAFRAME===> {len(filtered_df)}')
    else:
        filtered_df = df
    
    filtered_df['ca_updated'] = False
    filtered_df['el_updated'] = False

    for name in filtered_df['full_name'].unique():
        early_life, career = wiki_enrich(name)

        if early_life is not None:
            filtered_df.loc[filtered_df['full_name']==name,'early_life'] =early_life
            filtered_df.loc[filtered_df['full_name']==name,'el_updated'] =True

        if career is not None:
            filtered_df.loc[filtered_df['full_name']==name,'career'] =early_life
            filtered_df.loc[filtered_df['full_name']==name,'ca_updated'] =True

        

    print(filtered_df)
    return filtered_df


def wiki_enrich(name):

    wiki_lang = wikipediaapi.Wikipedia(
        language="en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='DataSciencePortfolio/v1.0 (arfathsaleem@gmail.com)'
    )

    # Define the person's name or title you want to search for
    person_name = name  # Replace with the person's name

    # Fetch the Wikipedia page
    page = wiki_lang.page(person_name)

    career_section,early_life_section,summary = None,None,None

    # Check if the page exists
    if page.exists():
        # Access the "Early life and education" section
        early_life_section = None
        summary = page.summary
        for section in page.sections:
            if "early life" in section.title.lower():
                early_life_section = section

            if "career" in section.title.lower():
                career_section = section

                break
        
    result_1 = early_life_section.text[:3000] if early_life_section else summary
    result_2 = career_section.text[:3000] if career_section else summary

    if summary:
        return result_1, result_2
    else: 
        print(f'Page not found for {name}')
        return 'page not found','page not found'



if __name__ == "__main__":
    # wiki_enrich('Barak Obama')
    batch_size = 150
    
    df = pd.read_csv("BillionaireListCleaned.csv")
    write_file = 'BillionairesWikiEnriched.csv'

    df = df[df['listing_instance']=='First']

    print(len(df))
    batch_max = int(len(df)/batch_size)

    print(df.columns)


    for batch in range(batch_max):
        batch_start = batch*batch_size
        batch_end = batch_start+batch_size
        partial_df = df[batch_start:batch_end]

        # print(f'PARTIAL UID {partial_df["UID"]}')
        write_df = enrich_csv(partial_df,write_file)
        write_to_csv(write_df,write_file)
        print(f'Batch {batch+1}/{batch_max}: COMPLETE')
        time.sleep(60)