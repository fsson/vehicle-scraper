import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

def get_urls(url, limiter):
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and limiter in href:
            urls.append(href)
    return urls

def get_all_urls():

    # Get all immediately availible links to all Tyresö ZIP code pages
    print('Fetching all availible first-level ZIP code pages...')
    initial_urls = get_urls('https://www.bolagsfakta.se/foretag/tyres%C3%B6-kommun', 'foretag/tyres%C3%B6-kommun/')

    # Get additional links from pages with page navigation
    additional_urls = []
    index = 1
    for i in initial_urls:
        print(f'Checking for page navigation ({index}/{len(initial_urls)})', end='\r', flush=True)
        second_level_urls = get_urls(i, 'foretag/tyres%C3%B6-kommun/')
        index += 1
        for j in second_level_urls:
            additional_urls.append(j)
    print()

    # Get all company links from all ZIP code links
    all_urls = initial_urls + additional_urls
    all_company_urls = []
    index = 1
    for i in all_urls:
        print(f'Fetching company pages from ZIP code pages ({index}/{len(all_urls)})', end='\r', flush=True)
        company_urls = get_urls(i, 'bolagsfakta.se/')
        index += 1
        for j in company_urls:
            if j not in all_urls:
                all_company_urls.append(j)
    print()

    # Return all links to companies in Tyresö
    return all_company_urls

def car_count(company_url):

    # Construct car information URL
    url = company_url[:26] + '/foretag/fordon/' + company_url[27:]

    # Fetch page h2 title including number of cars
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    heading = soup.find('h2', class_='site-h3')

    # Return number of cars as int
    return int(heading.text.strip()[0])
    
if __name__ == "__main__":
    car_count('https://www.bolagsfakta.se/690607YEVE00001-Elfin_Power_System')