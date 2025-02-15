# ITAS256-Assignment-01

This repository contains three main Python scripts that work together to scrape IT job postings from two different websites—[ITJobs.ca](https://www.itjobs.ca/) and [TechTalent](https://jobs.techtalent.ca/)—and then combine them into a single JSON file. Additionally, the TechTalent postings are summarized using OpenAI’s GPT-4 model.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)


---

## Overview

1. **`main.py`**  
   - Imports scraping functions from `itjobs_data.py` and `techtalent_data.py`.
   - Collects job data from each source.
   - Combines the results into a single JSON (`joblist.json`) with the following structure:
     ```json
     {
       "itjobs": [
         {
           "position": "...",
           "company": "...",
           "location": "...",
           "description": "..."
         },
         ...
       ],
       "techtalent": [
         {
           "position": "...",
           "company": "...",
           "location": "...",
           "job_description_url": "...",
           "summary": "..."
         },
         ...
       ]
     }
     ```

2. **`itjobs_data.py`**  
   - Scrapes job postings from [ITJobs.ca](https://www.itjobs.ca/) for pages 1 to 7.
   - Extracts:
     - **Position**  
     - **Company**  
     - **Location**  
     - **Description**  
   - Returns a list of job postings as dictionaries.

3. **`techtalent_data.py`**  
   - Scrapes job postings from [TechTalent](https://jobs.techtalent.ca/) using **cloudscraper**.
   - Extracts:
     - **Position**  
     - **Company**  
     - **Location**  
     - **Job Description URL**  
   - Attempts (up to 3 times) to fetch and parse each job's detailed description.
   - Uses OpenAI’s GPT-4 model to generate summaries of the job descriptions.
   - Returns a list of job postings as dictionaries, including the GPT-4 summary.

---

## Features
- **Multi-Page Scraping**: Gathers IT job postings from multiple pages on both ITJobs.ca and TechTalent.
- **Job Description Summaries**: Summarizes TechTalent postings using GPT-4 for quick reference.
- **JSON Output**: Merges both datas into a single JSON file.
- **Rate-Limiting Friendly**: Uses random delays and `cloudscraper` to minimize the chance of being blocked.

---

## Prerequisites
- **Python** 

### Python Libraries
- `requests`
- `beautifulsoup4`
- `certifi`
- `cloudscraper`
- `fake_useragent`
- `openai`
- `python-dotenv`

---

## Installation

1. **Clone the repository**:
   ```bash
   https://github.com/anexinwilson/anexin.wilson-ITAS256-A01.git
   cd anexin.wilson-ITAS256-A01

  **Installing packages**
Run 'pip install -r requirements.txt'

## Usage

### Set up Environment Variables
(See [Environment Variables](#environment-variables) below)

1. **Create  `.env` file** in the project directory and add  OpenAI API key:
   ```ini
   OPENAI_API_KEY='openai_key_here'

## Run the Program
py main.py


