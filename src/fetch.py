import cloudscraper
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm

scraper = cloudscraper.create_scraper()

# Functions for getting all availible href links from a given page
def get_urls(url, limiter):
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and limiter in href:
            urls.append(href)
    return urls

# Function for getting all URLs to all companies in Tyresö
def get_all_urls():

    # Get all immediately availible links to all Tyresö ZIP code pages
    print('Fetching all availible first-level ZIP code pages...')
    initial_urls = get_urls('https://www.bolagsfakta.se/foretag/tyres%C3%B6-kommun', 'foretag/tyres%C3%B6-kommun/')

    # Get additional links from pages with page navigation
    additional_urls_lists = multi_thread_fetch(
        lambda url: get_urls(url, 'foretag/tyres%C3%B6-kommun/'),
        initial_urls,
        'Fetching additional page navigation links'
    )

    # Flatten result
    additional_urls = [j for sublist in additional_urls_lists for j in (sublist or [])]

    # Get all company links from all ZIP code links
    all_urls = initial_urls + additional_urls
    company_urls_lists = multi_thread_fetch(
        lambda url: get_urls(url, 'bolagsfakta.se/'),
        all_urls,
        'Fetching all company page links'
    )

    # Flatten result, leaving out page navigation links
    all_company_urls = [j for sublist in company_urls_lists for j in (sublist or []) if j not in all_urls]

    # Return all links to companies in Tyresö
    return all_company_urls

# Function for getting text from specified tag and class
def get_data_from_html_tag(url, html_tag, html_class):
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    heading = soup.find(html_tag, class_=html_class)
    if heading:
        return heading.text.strip()
    return None

# Function for getting company name
def name(company_url):

    # Fetch company name from h1 title
    company_name = get_data_from_html_tag(company_url, 'h1', 'site-h1--small')
    if company_name:
        return company_name
    return None

# Function for getting company car count
def car_count(company_url):
    
    # Construct car information URL
    url = company_url[:26] + '/foretag/fordon/' + company_url[27:]

    # Fetch and return number of cars from h2 title
    number_of_cars_h2 = get_data_from_html_tag(url, 'h2', 'site-h3')
    if number_of_cars_h2:
        number_of_cars = number_of_cars_h2.split()[0]
        return int(number_of_cars)
    return None

# Function for fetching name and car count for each company
def company_data(urls):

    # Wrapper function for running on multiple threads
    def wrapper_function(url):
        company_name = name(url)
        number_of_cars = car_count(url)
        if company_name and number_of_cars:
            return company_name, number_of_cars
    
    # Get name and car count for each company
    all_company_data_lists = multi_thread_fetch(
        lambda url: wrapper_function(url),
        urls,
        'Extracting company name and number of cars from company pages'
    )

    # Flatten result
    all_company_data = [j for sublist in all_company_data_lists for j in (sublist or [])]

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