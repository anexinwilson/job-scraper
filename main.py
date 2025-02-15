from itjobs_data import scrape_itjobs
from techtalent_data import scrape_techtalent
from json import dumps

def main():
    
    itjobs_posts = scrape_itjobs()
    techtalent_posts = scrape_techtalent()
    # combined dumping to json for both itjob and techtalent so that techtalent jobs won't overwrite the itjobs from json file
    itjobs_and_techtalent = {"itjobs": itjobs_posts, "techtalent": techtalent_posts}

    with open("joblist.json", "w") as json_file:
        json_file.write((dumps(itjobs_and_techtalent, indent=2)))

if __name__ == "__main__":
    main()



