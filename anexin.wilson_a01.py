import requests
from bs4 import BeautifulSoup
import certifi
from json import dumps
import cloudscraper

itjobs_base_url = "https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page="
techtalent_url = 'https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada'
techtalent_base_url = 'https://jobs.techtalent.ca'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

headers = {'User-Agent': USER_AGENT}

itjobs_job_postings = []

for page in range(1, 8):
    itjobs_url = itjobs_base_url + str(page)
    itjobs_page = requests.get(itjobs_url, headers=headers, verify=certifi.where())

    itjobs_soup = BeautifulSoup(itjobs_page.content, "html.parser")
    results = itjobs_soup.find('div', class_='result-ctn content')
    itjobs_cards = results.find_all('div', class_='result-item external')

    for itjob in itjobs_cards:
        itjob_position = itjob.find('a', class_='offer-name').contents[0].strip()
        itjob_company = itjob.find('a', class_='company').text.strip()
        itjob_location = itjob.find('a', class_='location').text.strip()
        itjob_description = itjob.find('p', class_='offer-description').text.strip()
        
        itjobs_job_postings.append({
            "position": itjob_position,
            "company": itjob_company,
            "location": itjob_location,
            "description": itjob_description
        })

# Part 2 

# Used cloudscraper to enable javascript and cookies to continue to scrape from tech talent
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows"
    }
)

# techtalent_page = requests.get(techtalent_baseurl, headers=headers, verify=certifi.where())
response = scraper.get(techtalent_url, headers=headers, verify=certifi.where())
techtalent_soup = BeautifulSoup(response.text, "html.parser")

# print(techtalent_soup)
result = techtalent_soup.find('div', class_='jobContainer')
# print(result)

techtalent_description_link = result.find_all('a', class_='job-post-summary w-full no-underline block text-grey-darkest mb-2 mb-3 border bg-white rounded-lg')

techtalent_description_urls = []
for links in techtalent_description_link:
    techtalent_description_urls.append(techtalent_base_url + links.get('href'))


techtalent_jobs_cards = result.find_all('div', class_='whitespace-normal')


# created an empty list to store the techtalent jobs
techtalent_job_posts = []

# Using index to create a counter to match the techtalent data with its urls, and len() to get the number of content for each, and range() to loop for that amount of number
for index in range(len(techtalent_jobs_cards)):
    # used to store the data from techtalent_job as a list in index 
    techtalent_job = techtalent_jobs_cards[index]
     # used to store the data from techtalent_ as a list in index 
    techtalent_description_url = techtalent_description_urls[index]
    techtalent_job_position = techtalent_job.find('h2', class_='job-post-summary__title text-base').text.strip()
    techtalent_company = techtalent_job.find('span', class_='flex items-center mir-2 no-underline w-full mb-2 md:w-auto md:mb-0').contents[-1].strip()
    techtalent_job_location = techtalent_job.find('span', class_='flex flex-shrink items-center').text.strip()


    # dictionary values will be added to empty list
    techtalent_job_posts.append({
        "position": techtalent_job_position,
        "company": techtalent_company,
        "location": techtalent_job_location,
        "job_description_url": techtalent_description_url  # Added job description URL
    })

# combined dumping to json for both itjob and techtalent so that techtalent jobs won't overwrite the itjobs from json file
itjobs_and_techtalent = {"itjobs": itjobs_job_postings, "techtalent": techtalent_job_posts}

with open("joblist.json", "w") as json_file:
    json_file.write((dumps(itjobs_and_techtalent, indent=2)))



