# What it takes to be a Billionaire

Brief Description of the Project
- This engaging project aims to analyze the common background factors of billionaires from 1997 to 2003.
- The goal is to create insightful visualizations in Tableau, highlighting key patterns and information.
- Currently, I'm in the process of data cleaning and preparation for analysis. Updates on this project will be posted regularly.


**Stage 1: Data Gathering and Cleansing**

Key Activities

   Public Data Cleaning & Preparation for Data Visualization
_   Focusing on making the data visualization-ready._
   Using the Wikipedia API for Data Enrichment
 _  Enhancing the dataset with additional details from Wikipedia._
   Leveraging OpenAI API to Structure Unstructured Data
_   Converting unstructured Wikipedia data into a format suitable for analysis._


What it takes to be a billionaire - Graphical visualization project

1. Initial Dataset
   - Initial Dataset taken from Forbes Billionaire Evolution - https://www.gigasheet.com/sample-data/forbes-billionaires-evolution-1997-2023

2. Cleaning - Step 1: [Initial Preparation](/billionaireslistclean.py)
   - Initial Data cleansing achieved the following objectives:
      - Eliminate Data inconsistencies (Industry Names, Full Name format, Age, Birth Year)
      - Additional columns for classification: Age Category, First Time a Billionaire on Forbes?
      - Identify blank / unavailable data
   - Output file - [BillionaireListCleaned.csv](/BillionaireListCleaned.csv)
  
3. Cleaning - Step 2: [Wikipedia Enrichment](/wikipedia_enrich.py)
   -Intended Objectives: Gather information to find out the following:
               - were they self-made or did they inherit? 
               - what is their highest education background? 
               - what is their country of birth? Only give the country name
               - What got them to being a billionaire (entrepreneurship, investment, inheritance, althletics, media personality...etc)?
   - Enrich each person's information using the Wikipedia API. Objectives achieved:
      - Early Life, Career and Summary Sections Enriched via Wikipedia API
   - Output file - [BillionairesWikiEnriched](/BillionairesWikiEnriched.csv)
  
4. Cleaning - Step 3: [GPT Enrichment](/BillionairesGPTEnriched.csv)
   - Objectives: Understand the data taken from Wikipedia and categorize them for quantitative analysis
      - 
