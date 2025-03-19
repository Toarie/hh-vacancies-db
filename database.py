import psycopg2
from config import DB_CONFIG


def create_tables():
    """
    Создает таблицы в базе данных PostgreSQL.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Создание таблицы employers
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            website VARCHAR(255)
        )
    """)

    # Создание таблицы vacancies
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INT REFERENCES employers(employer_id),
            title VARCHAR(255) NOT NULL,
            salary_from INT,
            salary_to INT,
            currency VARCHAR(10),
            url VARCHAR(255)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_employer_data(conn, employer_data):
    """
    Вставляет данные о компании в таблицу employers.
    :param conn: Соединение с базой данных
    :param employer_data: Данные о компании
    :return: ID компании в базе данных
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employers (name, description, website)
        VALUES (%s, %s, %s)
        RETURNING employer_id
    """, (employer_data['name'], employer_data['description'], employer_data['site_url']))
    employer_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return employer_id


def insert_vacancy_data(conn, vacancy_data, employer_id):
    """
    Вставляет данные о вакансиях в таблицу vacancies.
    :param conn: Соединение с базой данных
    :param vacancy_data: Данные о вакансиях
    :param employer_id: ID компании в базе данных
    """
    cur = conn.cursor()
    for vacancy in vacancy_data:
        salary_from = vacancy['salary']['from'] if vacancy['salary'] else None
        salary_to = vacancy['salary']['to'] if vacancy['salary'] else None
        currency = vacancy['salary']['currency'] if vacancy['salary'] else None

        cur.execute("""
            INSERT INTO vacancies (employer_id, title, salary_from, salary_to, currency, url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (employer_id, vacancy['name'], salary_from, salary_to, currency, vacancy['alternate_url']))
    conn.commit()
    cur.close()
