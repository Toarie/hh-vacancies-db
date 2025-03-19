import requests

def get_employer_data(employer_id):
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_vacancies_data(employer_id):
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return None

