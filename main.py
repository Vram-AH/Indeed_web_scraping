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


def get_total_pages():
    params = {
        'q': 'Python Developer',
        'l': 'New York State',
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
    print(total)

def get_all_items():
    params = {
        'q': 'Python Developer',
        'l': 'New York State',
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

    with open('json_result/job_list.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)
    print('json created')

    #create CSV and Excel file
    df = pd.DataFrame(jobs_list)
    df.to_csv('indeed_data.CSV', index=False)
    df.to_excel('indeed_data.xlsx', index=False)

    # data created
    print('Data Created Success')




if __name__ == '__main__':
    get_all_items()
