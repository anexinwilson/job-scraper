import requests
from bs4 import BeautifulSoup
import certifi
from json import dumps
import cloudscraper

def scrape_itjobs():
    base_url = "https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page="
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

    headers = {'User-Agent': USER_AGENT}

    itjobs_job_postings = []

    for page in range(1, 8):
        itjobs_url = base_url + str(page)
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

    return itjobs_job_postings