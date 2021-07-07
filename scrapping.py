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
    link_tag = card.h2.a
    job_title = link_tag.get('title')
    job_url = 'https://www.indeed.com' + link_tag.get('href')
    company = card.find('span', 'company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div', 'summary').text.strip()
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        job_salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        job_salary = ''

    record = (job_title, company, job_location, post_date,
              today, job_summary, job_salary, job_url)

    return record


def main(position, location):
    records = []
    url = get_url(position, location)
    print(url)
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('div', 'jobsearch-SerpJobCard')

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
        writer.writerow(['Titre', 'Entreprise', 'Localisation', 'Date du poste',
                        'Date d\'extraction', 'Résumé', 'Salaire', 'Url'])
        writer.writerows(records)


main('Stagiaire Développement', 'Toulouse (31)')
