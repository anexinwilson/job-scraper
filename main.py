"""
This function combines job postings  from ITJobs and TechTalent into a single JSON file.
It imports scraping functions from 'itjobs_data.py' and 'techtalent_data.py', calls these functions
to retrieve job postings, and then writes the combined data into joblist.json.
"""



# Import the function to scrape IT Jobs data from the itjobs_data.py
from itjobs_data import scrape_itjobs
# Import the function to scrape TechTalent data from the techtalent_data.py
from techtalent_data import scrape_techtalent
# Import dumps to convert python object to json
from json import dumps

def main():
    # Scrape job posts from IT Jobs
    itjobs_posts = scrape_itjobs()
    # Scrape job posts from Techtalent Jobs
    techtalent_posts = scrape_techtalent()
    # combined dumping to json for both itjob and techtalent so that techtalent jobs won't overwrite the itjobs from json file
    itjobs_and_techtalent = {"itjobs": itjobs_posts, "techtalent": techtalent_posts}

#    open the json in write mode
    with open("joblist.json", "w") as json_file:
        # add the list dictionary from to the json file
        json_file.write((dumps(itjobs_and_techtalent, indent=2)))

# To ensure that the main.py can only be run from this file
if __name__ == "__main__":
    main()



