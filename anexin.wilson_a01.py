import requests
from bs4 import BeautifulSoup
import certifi
from json import dumps
import cloudscraper



itjobs_base_url = "https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page="
techtalent_baseurl = 'https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

headers = {'User-Agent':USER_AGENT}

itjobs_job_postings= []

for page in range(1,8):
    itjobs_url = itjobs_base_url + str(page)
    itjobs_page = requests.get(itjobs_url,headers=headers , verify=certifi.where())

    itjobs_soup = BeautifulSoup(itjobs_page.content,"html.parser")
    results = itjobs_soup.find('div',class_ ='result-ctn content')
    # print(results)
    itjobs_cards = results.find_all('div',class_='result-item external')

    for itjob in itjobs_cards:
        itjob_position = itjob.find('a', class_='offer-name').contents[0].strip()
        itjob_company = itjob.find( 'a', class_='company').text.strip()
        itjob_location = itjob.find('a', class_='location').text.strip()
        itjob_description = itjob.find('p', class_ = 'offer-description').text.strip()
        # print(f'Position: {itjob_position} is for company {itjob_company} in {itjob_location} and job description is {itjob_description} \n \n')
        itjobs_job_postings.append({"position":itjob_position,"company":itjob_company,"location":itjob_location,"description":itjob_description})



# Part 2 

# Used cloudscraper to enable javascript and cookies to continue to scrape from tech talent
scraper = cloudscraper.create_scraper(
    browser = {
        "browser":"chrome",
        "platform":"windows"
    }
)


# techtalent_page =  requests.get(techtalent_baseurl,headers=headers,verify=certifi.where())
response = scraper.get(techtalent_baseurl,headers=headers, verify=certifi.where())
techtalent_soup = BeautifulSoup(response.text,"html.parser")
# print(techtalent_soup)
result =  techtalent_soup.find('div',class_='jobContainer')
# print(result)
techtalent_jobs_cards = result.find_all('div',class_='whitespace-normal')


# print(techtalent_jobs_cards)

# created an empty list to store the techtalent jobs
techtalent_job_posts = []

for techtalent_job in techtalent_jobs_cards:
    techtalent_job_position = techtalent_job.find('h2',class_='job-post-summary__title text-base').text.strip()
    techtalent_company = techtalent_job.find('span',class_='flex items-center mir-2 no-underline w-full mb-2 md:w-auto md:mb-0').contents[-1].strip()
    techtalent_job_location = techtalent_job.find('span',class_='flex flex-shrink items-center').text.strip()
    # print(techtalent_job_position,techtalent_job_location)

    # dictionary values will be added to empty list
    techtalent_job_posts.append({"position":techtalent_job_position,"company":techtalent_company,"location":techtalent_job_location})

# combined dumping to json for both itjob and techtalent so that techtalent jobs wont overwrite the itjobs from json file
itjobs_and_techtalent = {"itjobs":itjobs_job_postings, "techtalent": techtalent_job_posts}

with open("joblist.json","w") as json_file:
    json_file.write((dumps(itjobs_and_techtalent,indent=2)))


