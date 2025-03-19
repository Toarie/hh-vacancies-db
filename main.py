from api import get_employer_data, get_vacancies_data
from database import create_tables
from db_manager import DBManager
import psycopg2
from config import DB_CONFIG


def main():
    # Создание таблиц
    create_tables()

    # Получение данных о компаниях и вакансиях
    employer_ids = ["1", "2", "3", ...]  # ID компаний с hh.ru
    conn = psycopg2.connect(**DB_CONFIG)

    for employer_id in employer_ids:
        employer_data = get_employer_data(employer_id)
        if employer_data:
            employer_id_db = insert_employer_data(conn, employer_data)
            vacancies_data = get_vacancies_data(employer_id)
            if vacancies_data:
                insert_vacancy_data(conn, vacancies_data, employer_id_db)

    # Работа с DBManager
    db_manager = DBManager()

    print("Компании и количество вакансий:")
    print(db_manager.get_companies_and_vacancies_count())

    print("\nВсе вакансии:")
    print(db_manager.get_all_vacancies())

    print("\nСредняя зарплата:")
    print(db_manager.get_avg_salary())

    print("\nВакансии с зарплатой выше средней:")
    print(db_manager.get_vacancies_with_higher_salary())

    print("\nВакансии с ключевым словом 'python':")
    print(db_manager.get_vacancies_with_keyword("python"))

    db_manager.close()


if __name__ == "__main__":
    main()

