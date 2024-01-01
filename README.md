# Billionaires - What it takes to be one

Key Activities
1. Public Data Cleaning & Preparing for Data Visualization
2. Use of Wikipedia API for data enrichment
3. Use of OpenAI API to clean the unstructured information gathered from Wikipedia into structured data for better analysis

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
   - In
