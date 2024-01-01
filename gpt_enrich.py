from openai import OpenAI
import os
import csv
import pandas as pd
import numpy as np

"""
GPT Model	                    Input	                        Output
gpt-3.5-turbo-1106	        $0.0010 / 1K tokens	            $0.0020 / 1K tokens
"""

API_KEY = None #ADD API KEY HERE

if API_KEY is not None:
    os.environ['OPENAI_API_KEY'] = API_KEY
else:
    "OpenAI API KEY Unavailable"

gpt_model = "gpt-3.5-turbo-1106"


def prompt_gpt(prompt_description):
    # output_message = 'this is a test'
    # total_cost = 'this is a test'
    client = OpenAI()

    task = """
    Here's your task:
    Based on the given description answer the following. Make sure to only provide answers from the given options:
                - are they self-made or did they inherit? answer options: “Self Made”, “Not Self Made”, “Unsure”
                - what is their highest education background?  answer options: “Did not complete high school”, “High School diploma”, “Bachelor’s Degree”, “Masters Degree”, “PhD”, “Unknown”
                - what is their country of birth? Only give the country name
                - What got them to being a billionaire? Give a one word answer such as - inheritance, entrepreneurship, Acting, Athlete, other...?            
                
    """
    description = f"Here's the Description: {prompt_description}"

    completion = client.chat.completions.create(
    model=gpt_model,
    messages=[
        {"role": "system", 
        "content": "you are a data assistant. you will be summarizing the given description into structured data as described",

        },
        {
            "role":"user",
            "content":task+description
        }

    ]
    )

    output_message = completion.choices[0].message

    print(completion.choices[0].message)
    print(completion.usage)

    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens

    input_cost = 0.001*(input_tokens/1000)
    output_cost = 0.002*(output_tokens/1000)

    total_cost = input_cost+output_cost

    print('total cost = $',round(total_cost,5))
    print('input cost = $',round(input_cost,5))
    print('output cost = $',round(output_cost,5))

    
    return output_message, total_cost

def enrich_rows(row):

    print(row['UID'])

    early_life_str = str(row['early_life'])
    career_str = str(row['career'])
    

    if len(early_life_str)>=2800:
        prompt_description = early_life_str
    else:
        prompt_description = early_life_str+" "+career_str
    
    gpt_response, total_cost = prompt_gpt(prompt_description)

    return pd.Series({'gpt_response': gpt_response, 'total_cost': total_cost})

def enrich_csv(df,output_file):
    
    
    headers = list(df.columns) + ['gpt_response','total_cost']

    file_exists = os.path.exists(output_file)

    if not file_exists:
        with open(output_file,'w',newline='' ) as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    
    if file_exists:
        check_df = pd.read_csv(output_file, dtype={'UID': str})

        # print('checkdf complete')
        # print(check_df["full_name"].head(10))

    if file_exists:
        print(f'Existing DATAFRAME===> {len(df)}')
        filtered_df = df[~df['UID'].isin(check_df['UID'])]
        
    else:
        filtered_df = df


    final_df = filtered_df[filtered_df['early_life'] != 'page not found']

    print(final_df.head(10))

    print(f'DATA FRAME TO PROCESS===> {len(final_df)}')

    # Apply the function to each row
    enriched_df = final_df.apply(enrich_rows, axis=1)

    # Check if the expected columns are in the resulting DataFrame
    if 'gpt_response' in enriched_df and 'total_cost' in enriched_df:
        final_df.loc[:, 'gpt_response'] = enriched_df['gpt_response']
        final_df.loc[:,'total_cost'] = enriched_df['total_cost']
    else:
        print("Expected columns not found in the enriched DataFrame")

    
    print(final_df.head())
    return final_df


def write_to_csv(df,file_name):
    #append dataframe to file without header
    with open(file_name,'a',newline='') as file:
        df.to_csv(file,mode='a',header=False,index=False)

if __name__ == "__main__":
    input_file = 'BillionairesWikiEnriched.csv'
    output_file = 'BillionairesGPTEnriched.csv'

    df = pd.read_csv(input_file)

    print("LENGTH OF DF===>",len(df))
    # df = df[0:40]
    print("LENGTH OF DF===>",len(df))

    batch_size = 10
    batches = round(len(df)/batch_size)

    print("BATCHES ===> ",batches)

    for batch in range(batches):
        batch_start = batch*batch_size
        batch_end = batch_start+batch_size
        enriched_df = enrich_csv(df[batch_start:batch_end],output_file)
        write_to_csv(enriched_df,output_file)
        print(f"~~~~~~~~~~BATCH {batch+1}/{batches} done...")