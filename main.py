from src import fetch
import csv

def write_to_csv(data):
    with open ('data.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Company', 'Registered vehicles'])
        for company_name, car_count in sorted(data, key=lambda x: x[1], reverse=True):
            writer.writerow([company_name, car_count])

if __name__ == "__main__":
    urls = fetch.get_all_urls()
    data = fetch.company_data(urls)
    write_to_csv(data)
    print('Company car data successfully saved to CSV')