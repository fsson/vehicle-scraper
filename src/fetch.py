import cloudscraper
import requests
from bs4 import BeautifulSoup
import re

def get_urls(url, limiter='foretag/tyres%C3%B6-kommun/'):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if limiter in href:
            urls.append(href)
    return urls

def get_all_urls():

    # Get all immediately availible links to all Tyresö ZIP code pages
    initial_urls = get_urls('https://www.bolagsfakta.se/foretag/tyres%C3%B6-kommun')

    # Get additional links from pages with page navigation
    additional_urls = []
    for i in initial_urls:
        second_level_urls = get_urls(i)
        for j in second_level_urls:
            additional_urls.append(j)

    # Get all company links from all ZIP code links
    all_urls = initial_urls + additional_urls
    all_company_urls = []
    for i in all_urls:
        company_urls = get_urls(i, 'bolagsfakta.se/')
        for j in company_urls:
            if j not in all_urls:
                all_company_urls.append(j)

    # Return all links to companies in Tyresö
    return all_company_urls

def car_count(company_url):

    # Fetch HTML circumventing cloudflare
    response = scraper.get(company_url)

    # Parse response and extract car # heading
    soup = BeautifulSoup(response.text, 'html.parser')
    heading = soup.find('h2', class_='site-h3')

    # Return # of cars as int
    return int(heading.text.strip()[0])
    
if __name__ == "__main__":
    for url in get_all_urls():
        print(url)