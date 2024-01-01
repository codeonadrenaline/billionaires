# What it takes to be a Billionaire

Brief Description of the Project
- This engaging project aims to analyze the common background factors of billionaires from 1997 to 2003.
- The goal is to create insightful visualizations in Tableau, highlighting key patterns and information.
- Currently, I'm in the process of data cleaning and preparation for analysis. Updates on this project will be posted regularly.


**Stage 1: Data Gathering and Cleansing**

Key Activities

   1. Public Data Cleaning & Preparation for Data Visualization
      - Focusing on making the data visualization-ready
   2. Using the Wikipedia API for Data Enrichment
      - Enhancing the dataset with additional details from Wikipedia
   3. Leveraging OpenAI API to Structure Unstructured Data
      - Converting unstructured Wikipedia data into a format suitable for analysis


Steps to Data Gathering and Cleansing

1. Initial Dataset
   -Sourced from Forbes [Billionaire Evolution 1997 - 2023](https://www.gigasheet.com/sample-data/forbes-billionaires-evolution-1997-2023)

2. Cleaning - Step 1: Initial Preparation
   - [**Script** - Initial Data Preparation](/billionaireslistclean.py)
   - **Achievements:**
         - Resolving data inconsistencies (e.g., Industry Names, Name Formats, Age, Birth Year)
         - Adding new classification columns: Age Category, First-Time Billionaire Status
         - Identifying and addressing missing data
   - **Output file** [BillionaireListCleaned.csv](/BillionaireListCleaned.csv)
  
4. Cleaning - Step 2: Wikipedia Enrichment
   - **Script:** [Wikipedia Enrichment](/wikipedia_enrich.py)
   - **Goals:**
         - Determine if billionaires are self-made or inherited wealth
         - Ascertain highest education level and country of birth
         - Identify the primary source of wealth (e.g., entrepreneurship, investment, inheritance)
   - **Achievements:**
         - Enhanced profiles with Early Life, Career, and Summary sections using Wikipedia API
   - **Output file** - [BillionairesWikiEnriched](/BillionairesWikiEnriched.csv)
  
5. Cleaning - Step 3: [GPT Enrichment](/BillionairesGPTEnriched.csv)
   - **Script:** [OpenAI Enrichment](/gpt_enrich.py)
   - **Goals**:
      - Categorize the data taken from Wikipedia for quantitative analysis
   - **Achievements**
      - Using the OpenAI API, Classifed the data to have the following information in place
        - are they self-made or did they inherit? answer options: “Self Made”, “Not Self Made”, “Unsure”
        - what is their highest education background?  answer options: “Did not complete high school”, “High School diploma”, “Bachelor’s Degree”, “Masters Degree”, “PhD”, “Unknown”
        - what is their country of birth? Only give the country name
        - What got them to being a billionaire? Give a one word answer such as - inheritance, entrepreneurship, Acting, Athlete, other...?
   - **Output file**- [GPTEnriched](/BillionairesGPTEnriched.csv)
