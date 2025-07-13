import cloudscraper
from bs4 import BeautifulSoup

# Fetch HTML circumventing cloudflare
scraper = cloudscraper.create_scraper()
response = scraper.get('https://www.bolagsfakta.se/foretag/fordon/5590266903-Prim_CC_AB')

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')
headings = soup.find('h2', class_='site-h3')

print(headings.text.strip()[0])