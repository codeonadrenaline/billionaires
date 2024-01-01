import csv
import pandas as pd
import re
import numpy as np


"""
ChatCompletionMessage(content=
'- are they self-made or did they inherit? \n  - Not Self Made
\n- what is their highest education background?  \n  - Bachelor’s Degree
\n- what is their country of birth? \n  - Kazakhstan
\n- What got them to being a billionaire? \n  - Entrepreneurship', 
role='assistant', function_call=None, tool_calls=None)
"""

def clean_records(row):
    cleaned_record = row['gpt_response'].replace("ChatCompletionMessage(content=","")
    cleaned_record = cleaned_record.replace(", role='assistant', function_call=None, tool_calls=None)","").replace("'","").replace("-","")
    substrings_to_keep = ['Self Made', 'Not Self Made','Inherit', 'Unsure']
    pattern = '|'.join(substrings_to_keep)


    education_substrings = ['High School', 'Bachelor', 'Masters', 'PhD', 'Unknown']
    education_pattern = '|'.join(education_substrings)

    result_selfmade = ' '.join(re.findall(pattern, cleaned_record))
    result_education = ' '.join(re.findall(education_pattern,cleaned_record))

    country_substrings = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", 
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", 
    "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", 
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", 
    "Congo, Republic of the", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czechia", 
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", 
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", 
    "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", 
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", 
    "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", 
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", 
    "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", 
    "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", 
    "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", 
    "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", 
    "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", 
    "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", 
    "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", 
    "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", 
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", 
    "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", 
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", 
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]

    country_pattern = '|'.join(country_substrings)
    result_country = ' '.join(re.findall(country_pattern,cleaned_record))

    return pd.Series({'self_made_wiki':result_selfmade,'highest_education':result_education,'birth_country':result_country})


def clean_gpt_response():
    df = pd.read_csv("BillionairesGPTEnriched.csv")

    df.info()

    new_columns_df = df.apply(clean_records,axis=1)

    df.loc[:,'self_made_wiki'] = new_columns_df['self_made_wiki']
    df.loc[:,'highest_education'] = new_columns_df['highest_education']
    df.loc[:,'birth_country'] = new_columns_df['birth_country']

    print(df.head(10))

    df.to_csv('FinalEnriched.csv')


if __name__ == "__main__":
    clean_gpt_response()