import requests
from bs4 import BeautifulSoup
import certifi
from json import dumps
import cloudscraper

def scrape_techtalent():

    url = 'https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada'
    base_url = 'https://jobs.techtalent.ca'

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

    headers = {'User-Agent': USER_AGENT}

    # Used cloudscraper to enable javascript and cookies to continue to scrape from tech talent
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows"
        }
    )

    # techtalent_page = requests.get(techtalent_baseurl, headers=headers, verify=certifi.where())
    response = scraper.get(url, headers=headers, verify=certifi.where())
    techtalent_soup = BeautifulSoup(response.text, "html.parser")

    # print(techtalent_soup)
    techtalent_results = techtalent_soup.find('div', class_='jobContainer')
    # print(result)

    techtalent_description_link = techtalent_results.find_all('a', class_='job-post-summary w-full no-underline block text-grey-darkest mb-2 mb-3 border bg-white rounded-lg')

    techtalent_description_urls = []
    for links in techtalent_description_link:
        techtalent_description_urls.append(base_url + links.get('href'))


    techtalent_jobs_cards = techtalent_results.find_all('div', class_='whitespace-normal')

    techtalent_page_descriptions = []
    for job_descriptions_url in techtalent_description_urls:
            description_page_response = scraper.get(job_descriptions_url,headers=headers,verify=certifi.where())
            techtalent_description_soup = BeautifulSoup(description_page_response.text,"html.parser")
            result = techtalent_description_soup.find('main',class_='bg-white p-4 sm:rounded-lg sm:border')
            description_result = techtalent_description_soup.find_all('div',class_='job-description-html')
            techtalent_page_descriptions.append(description_result)

            

    # created an empty list to store the techtalent jobs
    techtalent_job_posts = []

    # Using index to create a counter to match the techtalent data with its urls, and len() to get the number of content for each, and range() to loop for that amount of number
    for index in range(len(techtalent_jobs_cards)):
        # used to store the data from techtalent_job as a list in index 
        techtalent_job = techtalent_jobs_cards[index]
        # used to store the data from techtalent_ as a list in index 
        techtalent_description_url = techtalent_description_urls[index]
        techtalent_page_description = techtalent_page_descriptions[index]
        techtalent_job_position = techtalent_job.find('h2', class_='job-post-summary__title text-base').text.strip()
        techtalent_company = techtalent_job.find('span', class_='flex items-center mir-2 no-underline w-full mb-2 md:w-auto md:mb-0').contents[-1].strip()
        techtalent_job_location = techtalent_job.find('span', class_='flex flex-shrink items-center').text.strip()


        # dictionary values will be added to empty list
        techtalent_job_posts.append({
            "position": techtalent_job_position,
            "company": techtalent_company,
            "location": techtalent_job_location,
            "job_description_url": techtalent_description_url,
            "description": techtalent_page_description
        })

        return techtalent_job_posts