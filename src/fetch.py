import cloudscraper
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm

# Function for scraping webpage with cloudscraper
def web_scraper(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup:
        return soup
    return None

# Function for getting all availible href links from a given page
def get_urls(url, limiter):
    soup = web_scraper(url)
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and limiter in href:
            urls.append(href)
    return urls

# Function for getting all URLs to all companies in Tyresö
def get_all_urls():

    # Get all immediately availible links to all Tyresö ZIP code pages
    print('Fetching availible first-level ZIP code pages')
    initial_urls = get_urls('https://www.bolagsfakta.se/foretag/tyres%C3%B6-kommun', 'foretag/tyres%C3%B6-kommun/')

    # Get additional links from pages with page navigation
    additional_urls_lists = multi_thread_fetch(
        lambda url: get_urls(url, 'foretag/tyres%C3%B6-kommun/'),
        initial_urls,
        'Fetching page navigation links'
    )

    # Flatten result
    additional_urls = [j for sublist in additional_urls_lists for j in (sublist or [])]

    # Get all company links from all ZIP code links
    all_urls = initial_urls + additional_urls
    company_urls_lists = multi_thread_fetch(
        lambda url: get_urls(url, 'bolagsfakta.se/'),
        all_urls,
        'Fetching company page links'
    )

    # Flatten result, leaving out page navigation links
    all_company_urls = [j for sublist in company_urls_lists for j in (sublist or []) if j not in all_urls]

    # Return all links to companies in Tyresö
    return all_company_urls

# Function for getting company name and car count
def name_and_car_count(company_url):

    # Contstruct correct URL and scrape page
    url = company_url[:26] + '/foretag/fordon/' + company_url[27:]
    soup = web_scraper(url)
    full_soup = web_scraper(company_url)

    # Get company name from h1
    company_name_h1 = soup.find('h1', class_='site-h2')
    if company_name_h1:
        company_name = company_name_h1.text.strip().removeprefix('Fordon ägda av ')
    else:
        company_name = None

    # Get number of cars from h2
    number_of_cars_h2 = soup.find('h2', class_='site-h3')
    if number_of_cars_h2:
        number_of_cars = int(number_of_cars_h2.text.strip().split()[0])
    else:
        number_of_cars = None

    # Get phone number (if exists)
    phone_h2 = full_soup.find('h2', class_='site-h5', string='Telefon')
    phone_number = None
    if phone_h2:
        phone_p = phone_h2.find_next('p')
        if phone_p and phone_p.a:
            phone_number = phone_p.a.get_text(strip=True)

    if company_name and number_of_cars:
        return company_name, number_of_cars, phone_number
    return None

# Function for fetching name and car count for each company
def company_data(urls):
    
    # Get name and car count for each company running multiple threads
    all_company_data = multi_thread_fetch(
        lambda url: name_and_car_count(url),
        urls,
        'Fetching company car data'
    )

    # Return data on the number of cars for each company in Tyresö
    return all_company_data

# Function for calling functions with multiple threads
def multi_thread_fetch(function, urls, description):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        for result in tqdm(executor.map(function, urls), total=len(urls), desc=description):
            if result:
                results.append(result)
    return results
    
if __name__ == "__main__":
    pass