from src import fetch
import csv

def write_to_csv(data):
    with open ('data.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for company_name, car_count in data:
            writer.writerow([company_name, car_count])

if __name__ == "__main__":
    urls = fetch.get_all_urls()
    data = fetch.company_data(urls)
    write_to_csv(data)