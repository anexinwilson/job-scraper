"""
This file scrapes job postings from the TechTalent website and uses the OpenAI API 
to generate summaries of each job description.

It uses:
- cloudscraper and BeautifulSoup to retrieve and parse job data.
- python-dotenv to load environment variables (e.g., the OpenAI API key).
- fake_useragent to generate random User-Agent strings to reduce the risk of bot detection.
- certifi for for secure HTTPS requests.
- time and random to introduce delays between requests, helping avoid rate limits.
- os to interact with environment variables.
- The OpenAI API to summarize job descriptions.

The final output is a list of dictionaries, each containing a job's position, company, 
location, the URL to a job posting description page, and the generated summary.
"""




from bs4 import BeautifulSoup
import certifi
import cloudscraper
import time
import random
from fake_useragent import UserAgent
from openai import OpenAI 
import os
from dotenv import load_dotenv
import openai
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Set API Key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_job_description(description_text):
    """
    This function sends the provided job description text to the GPT-4 model 
    via the OpenAI API and returns a  summary.

    Args:
        description_text (str): The full job description text to be summarized.
    Returns:
        str or None: A short summary of the job description if successful; 
        otherwise, None.
    """
    try:
        # # make a request to chatgpt
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize this job description in a short paragraph:\n\n{description_text}"
                }
            ],
        )
        # Extract and return the summary from the response
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing job description:\n\n{e}\n")
        return None





def scrape_techtalent():
    """
    This function fetches the job listings page from TechTalent, extracts URLs for each 
    job's detailed description, and retrieves job information like position, company, location,URL to job description page.
    For each job, it has upto 3 attempts to fetch and parse the full job description, then 
    uses the OpenAI API to generate a concise summary of the description.

    The function returns list of dictionary::
                                    - "position": The job title.
                                    - "company": The company name.
                                    - "location": The job location.
                                    - "job_description_url": The URL linking to the full job description.
                                    - "summary": The concise summary generated from the full description.
    """
    url = 'https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada'
    base_url = 'https://jobs.techtalent.ca'

# create random user agent to prevent bot detection
    USER_AGENT = UserAgent()
    headers = {'User-Agent': USER_AGENT.random}

# Used cloudscraper to enable javascript and cookies to continue to scrape from tech talent
    scraper = cloudscraper.create_scraper(browser={
        "browser": "chrome",
        "platform": "windows"
        }
    )

# fetch the job listing page
    response = scraper.get(url, headers=headers, verify=certifi.where())
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find('div', class_='jobContainer')
    description_link = results.find_all('a',class_='job-post-summary w-full no-underline block text-grey-darkest mb-2 mb-3 border bg-white rounded-lg')

    # creating an empty list to store the job posting url to next page
    description_urls = []
    for links in description_link:
        # get the href from the <a> tag
        description_urls.append(base_url + links.get('href'))

    # Get the job details for all jobs
    jobs_cards = results.find_all('div', class_='whitespace-normal')

# create an empty list to store page description data
    page_descriptions = []
    for description_url in description_urls:
        retries = 3
        # give a javascript equivalent null to final_description
        final_description = None

# use loop for upto 3 attemtps to go to description page
        while retries > 0:
            try:
                # random delay between 15 to 60 second for each attempt to prevent from blocking for too much visit in a short time
                time.sleep(random.uniform(15, 60))
                # response to fetch the description page data
                job_description_response = scraper.get(description_url, headers={'User-Agent': USER_AGENT.random}, verify=certifi.where())
                # Parse job detail page with a new BeautifulSoup instance
                job_description_soup = BeautifulSoup(job_description_response.text, "html.parser")
                description_data = job_description_soup.find('div', class_='job-description-html')
                if description_data:
                    # Fetch all text from all elements in the div in a single string
                    final_description = " ".join(description_data.stripped_strings)
                    print(f"Fetched full description from: {description_url}")
                    break  # if a description_data found break from the loop
                else:
                    print(f"No job description found for {description_url}\n")
            except Exception as e:
                # if it is the 3 attempt and failed show error message
                if retries == 1:
                    print(f"Job:Error: {e}\n")
            finally:
                retries -= 1  # if last attempt is over break from the loop

    #    add the description data to the page_descriptions
        page_descriptions.append(final_description)


    # final list to store all data for the techtalent
    techtalent_job_posts = []

    # Using index to create a counter to match the techtalent data with its urls, and len() to get the number of content for each,
    #  and range() to loop for that amount of number
    for index in range(len(jobs_cards)):
        # used to store the data from techtalent_job as a list in index 
        techtalent_job = jobs_cards[index]
        # used to store the data from techtalent_ as a list in index 
        techtalent_description_url = description_urls[index]
        # used to store the data from page description to the summary text
        page_description = page_descriptions[index]

        techtalent_job_position = techtalent_job.find('h2', class_='job-post-summary__title text-base').text.strip()
        #  As the span element had multiple elements used .contents[-1] to get the last element which is the company name
        techtalent_company = techtalent_job.find('span', class_='flex items-center mir-2 no-underline w-full mb-2 md:w-auto md:mb-0').contents[-1].strip()
        techtalent_job_location = techtalent_job.find('span', class_='flex flex-shrink items-center').text.strip()
        summary_text = summarize_job_description(page_description)

        techtalent_job_posts.append({
            "position": techtalent_job_position,
            "company": techtalent_company,
            "location": techtalent_job_location,
            "job_description_url": techtalent_description_url,
            "summary": summary_text
        })

    return techtalent_job_posts


