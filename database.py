import psycopg2
from psycopg2 import sql
from config import DB_CONFIG
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def create_database():
    """
    Создает базу данных в PostgreSQL, используя параметры из DB_CONFIG.
    """
    try:
        # Подключаемся к серверу PostgreSQL (к базе данных postgres по умолчанию)
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        conn.autocommit = True  # Включаем автоматическое подтверждение транзакций
        cur = conn.cursor()

        # Проверяем, существует ли база данных
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(
            sql.Literal(DB_CONFIG['dbname'])
        ))
        exists = cur.fetchone()

        # Если база данных не существует, создаем её
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_CONFIG['dbname'])
            ))
            print(f"База данных {DB_CONFIG['dbname']} успешно создана.")
        else:
            print(f"База данных {DB_CONFIG['dbname']} уже существует.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


def create_tables():
    """
    Создает таблицы в базе данных PostgreSQL.
    """
    try:
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
        print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


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


if __name__ == "__main__":
    # Создаем базу данных и таблицы
    create_database()
    create_tables()


