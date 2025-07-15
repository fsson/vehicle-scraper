# Company vehicle scraper

This project is a Python web scraper for collecting data on registered vehicles per company in Tyresö kommun using data from [bolagsfakta.se](https://www.bolagsfakta.se/). It uses multi-threading to efficiently scrape large numbers of web pages in parallel, with the output saved in a CSV file.

## How it works

1. **Collect first-level links**: The scraper fetches all available ZIP code-based pages for Tyresö.
2. **Handle pagination**: The scraper identifies and follows all pagination links to ensure all companies are collected.
3. **Extract company links**: From each ZIP code and pagination page, the scraper extracts links to individual company profiles.
4. **Fetch vehicle data**: For each company, the scraper navigates to the company’s vehicle page and extracts:
   - The company name
   - The number of registered vehicles
5. **Save data to CSV**: All data is written to `data.csv`, sorted by vehicle count in descending order.

## Project structure

```bash
src/
  └── fetch.py   # All scraping functions
main.py          # Runs the full pipeline and saves results
data.csv         # Output file with company and vehicle data
```

## How to use
### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/vehicle-scraper.git
cd vehicle-scraper
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the scraper and generate CSV
```bash
python main.py
```
This will create a file named `data.csv` with the following format:

| Company            | Registered vehicles |
| ------------------ | ------------------- |
| Example AB         | 56                  |
| Another Company AB | 42                  |
