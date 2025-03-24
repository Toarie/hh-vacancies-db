from api import get_employer_data, get_vacancies_data
from database import create_database, create_tables, insert_employer_data, insert_vacancy_data
import psycopg2
from config import DB_CONFIG
from db_manager import DBManager


def main():
    # Создание базы данных и таблиц
    create_database()  # Теперь без параметров, берет данные из DB_CONFIG
    create_tables()

    # Список ID компаний с hh.ru
    employer_ids = [
        "15478",  # VK
        "1740",   # Яндекс
        "3529",   # Сбер
        "78638",  # Тинькофф
        "1122462",  # Ozon
        "41862",  # Ростелеком
        "3776",   # МТС
        "907345",  # Лаборатория Касперского
        "87021",  # 2ГИС
        "2180"    # Авито
    ]

    # Подключение к базе данных
    conn = psycopg2.connect(**DB_CONFIG)

    # Получение данных о компаниях и их вакансиях
    for employer_id in employer_ids:
        employer_data = get_employer_data(employer_id)
        if employer_data:
            employer_id_db = insert_employer_data(conn, employer_data)
            vacancies_data = get_vacancies_data(employer_id)
            if vacancies_data:
                insert_vacancy_data(conn, vacancies_data, employer_id_db)

    # Закрытие соединения с базой данных
    conn.close()

    # Работа с DBManager
    db_manager = DBManager()

    print("Компании и количество вакансий:")
    for company, count in db_manager.get_companies_and_vacancies_count():
        print(f"{company}: {count} вакансий")

    print("\nВсе вакансии:")
    for company, title, salary_from, salary_to, currency, url in db_manager.get_all_vacancies():
        salary = f"{salary_from or '?'}-{salary_to or '?'} {currency or ''}"
        print(f"{company}: {title} ({salary}) | {url}")

    avg_salary = db_manager.get_avg_salary()
    print(f"\nСредняя зарплата: {avg_salary:.2f}")

    print("\nВакансии с зарплатой выше средней:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(f"{vacancy[2]} (ID: {vacancy[0]})")

    print("\nВакансии с ключевым словом 'python':")
    for vacancy in db_manager.get_vacancies_with_keyword("python"):
        print(f"{vacancy[2]} (ID: {vacancy[0]})")

    db_manager.close()


if __name__ == "__main__":
    main()

