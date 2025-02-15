"""
This file scrapes job postings from the ITJobs.ca
It uses:
        - requests to fetch the HTML content of each page.
        - BeautifulSoup to parse the HTML and extract job data.
        - certifi to provide SSL certificates for secure HTTP requests.

The scraper iterates through pages 1 to 7, extracting for each job posting:
                                                                            - Job Position 
                                                                            - Company Name
                                                                            - Job Location
                                                                            - Job Description

The function returns a list of dictionaries, where each dictionary represents one job posting.
"""

import requests
from bs4 import BeautifulSoup
import certifi


def scrape_itjobs():
    """ 
    This function scrapes job postings from ITJobs.ca constructs URLs for pages 1 to 7 of ITJobs.ca, sends HTTP requests,
     and parses the HTML using BeautifulSoup. It then locates the container that holds the job
    postings, loops over each posting to extract the job title, company, location, and description, and
    stores the extracted data in a list of dictionaries.

    The functions returns a list of dictionary with:
                                    - "position": The job title.
                                    - "company": The company name.
                                    - "location": The job location.
                                    - "description": The job description.
    """


    base_url = "https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page="
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

    headers = {'User-Agent': USER_AGENT}

# create a empty list to store the itjob posting data
    itjobs_job_postings = []

# loop from 1 to 7 
    for page in range(1, 8):
        # get the itjob_url for each page by combining the base_url and loop for loop from 1 to 7
        itjobs_url = base_url + str(page) 
        itjobs_page = requests.get(itjobs_url, headers=headers, verify=certifi.where())

        # Parse HTML content using BeautifulSoup
        itjobs_soup = BeautifulSoup(itjobs_page.content, "html.parser")

        # find the main container in the page holding the job posting
        results = itjobs_soup.find('div', class_='result-ctn content')
        # find the container that has each of the individual job posting data
        itjobs_cards = results.find_all('div', class_='result-item external')


        # get job postings data as individual
        for itjob in itjobs_cards:
            # .content[0] is used as the a tag has two elements and the job name is in first element
            itjob_position = itjob.find('a', class_='offer-name').contents[0].strip()
            itjob_company = itjob.find('a', class_='company').text.strip()
            itjob_location = itjob.find('a', class_='location').text.strip()
            itjob_description = itjob.find('p', class_='offer-description').text.strip()

            # create a dictionary with the data and add it to itjobs_job_postings list
            itjobs_job_postings.append({
                "position": itjob_position,
                "company": itjob_company,
                "location": itjob_location,
                "description": itjob_description
            })

            

    return itjobs_job_postings