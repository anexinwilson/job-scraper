import requests
from bs4 import BeautifulSoup
import certifi


itjobs_url = "https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page=1"
techtalent_url = "https://jobs.techtalent.ca/?k=information%20technology&l=British%20Columbia,%20Canada"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

headers = {'User-Agent':USER_AGENT}

itjobs_page = requests.get(itjobs_url,headers=headers , verify=certifi.where())

itjobs_soup = BeautifulSoup(itjobs_page.content,"html.parser")
results = itjobs_soup.find('div',class_ ='result-ctn content')
# print(results)
itjobs_cards = results.find_all('div',class_='result-item external')
# itjob_position = results.find('a', class_='offer-name')


for itjob in itjobs_cards:
    itjob_position = itjob.find('a', class_='offer-name').contents[0].strip()
    itjob_company = itjob.find( 'a', class_='company').text.strip()
    itjob_location = itjob.find('a', class_='location').text.strip()
    itjob_description = itjob.find('p', class_ = 'offer-description').text.strip()
    print(f'Position: {itjob_position} is for company {itjob_company} in {itjob_location} and job description is {itjob_description} \n \n')


# print(itjobs_soup)

# print('\n \n \n end of it jobs page testing \n \n \n \n \n \n')

techtalent_page = requests.get(techtalent_url,headers = headers ,verify = certifi.where())
techtalent_soup = BeautifulSoup(techtalent_page.content,"html.parser")
# print(techtalent_soup)
