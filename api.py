import requests

def get_employer_data(employer_id):
    """
    Получает данные о компании по её ID через API hh.ru.
    :param employer_id: ID компании на hh.ru
    :return: Данные о компании в формате JSON или None, если запрос не удался
    """
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_vacancies_data(employer_id):
    """
    Получает список вакансий компании по её ID через API hh.ru.
    :param employer_id: ID компании на hh.ru
    :return: Список вакансий в формате JSON или None, если запрос не удался
    """
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return None
