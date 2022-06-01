import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.indeed.com/jobs?'
site = 'https://www.indeed.com'
params = {
    'q': 'Python Developer',
    'l': 'new york'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}

res = requests.get(url, params=params, headers=headers)
# print(res.status_code) = untuk tes web bisa scrapping atau tidak


def get_total_pages(query, location):
    params = {
        'q': query,
        'l': location,
        'vjk': '58789b4c15174434'
    }

    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    total_pages = []
    # scraping Step
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)

    total = int(max(total_pages))
    return total

def get_all_items(query, location, start, page):
    params = {
        'q': query,
        'l': location,
        'start': start,
        'vjk': '58789b4c15174434'
    }
    res = requests.get(url, params=params, headers=headers)

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

    #scraping process
    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')

    jobs_list = []
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName')
        company_name = company.text
        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link is not Available'

        #sorting data
        data_dict = {
            'title': title,
            'company name': company_name,
            'link': company_link
        }
        jobs_list.append(data_dict)

    #writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open(f'json_result/{query}_in_{location}_page_{page}.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)
    print('json created')
    return jobs_list

def create_document(dataFrame, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_results{filename}.xlsx', index=False)

    print(f'File {filename}.csv and {filename}.xlsx successfully craeted')


def run():
    query = input('Enter Your Query: ')
    location = input('Enter Your Location: ')

    total = get_total_pages(query, location)
    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_all_items(query, location, counter, page)

    # formating data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data Json Created')

    # create doucument
    create_document(final_result, query)


if __name__ == '__main__':
    run()
