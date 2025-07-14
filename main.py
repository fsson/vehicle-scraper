from src import fetch

def fetch_iterator():
    all_data = []
    page = 1
    while fetch.company_data(page):
        print(f"Fetching from page {page}", end="\r")
        all_data.extend(fetch.company_data(page))
        page += 1
    return all_data

if __name__ == "__main__":
    print(fetch_iterator())