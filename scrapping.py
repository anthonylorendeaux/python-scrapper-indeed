import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_url(position, location):
    template_url = 'https://fr.indeed.com/jobs?q={}&l={}'

    # Generate a url for scrapping
    url = template_url.format(position, location)
    return url


def get_record(card):
    job_title = card.find('h2', 'jobTitle').text.strip()
    job_url = 'https://www.indeed.com' + card['href']
    company = card.find('span', 'companyName').text.strip()
    job_location = card.find('div', 'companyLocation').text.strip()
    post_date = card.find('span', 'date').text.strip()
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        job_summary = card.find('div', 'job-snippet').find('li').text
    except AttributeError:
        job_summary = ''

    try:
        job_salary = card.find('span', 'salary-snippet').text.strip()
    except AttributeError:
        job_salary = ''

    record = (job_title, company, job_location, job_summary, post_date,
              today, job_salary, job_url)

    return record


def main(position, location):
    records = []
    url = get_url(position, location)
    print(url)
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('a', 'resultWithShelf')

        for job in jobs:
            record = get_record(job)
            records.append(record)
        try:
            url = 'https://fr.indeed.com' + \
                soup.find('a', {'aria-label': 'Suivant'}).get('href')
        except AttributeError:
            break

    # save the job data
    with open('indeed.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Titre', 'Entreprise', 'Localisation', 'Résumé', 'Date du poste',
                        'Date d\'extraction', 'Salaire', 'Url'])
        writer.writerows(records)

main('Stagiaire Développement', 'Toulouse (31)')
