import psycopg2
from config import DB_CONFIG


class DBManager:
    """
    Класс для работы с базой данных PostgreSQL.
    """

    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список кортежей (название компании, количество вакансий)
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id) 
            FROM employers e 
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id 
            GROUP BY e.name
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        :return: Список кортежей (название компании, название вакансии, зарплата от, зарплата до, валюта, ссылка)
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.currency, v.url 
            FROM vacancies v 
            JOIN employers e ON v.employer_id = e.employer_id
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return: Средняя зарплата (float)
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT AVG((salary_from + salary_to) / 2) 
            FROM vacancies 
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        """)
        result = cur.fetchone()[0]
        cur.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Список кортежей с данными о вакансиях
        """
        avg_salary = self.get_avg_salary()
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM vacancies 
            WHERE (salary_from + salary_to) / 2 > %s
        """, (avg_salary,))
        result = cur.fetchall()
        cur.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        :param keyword: Ключевое слово для поиска
        :return: Список кортежей с данными о вакансиях
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM vacancies 
            WHERE title ILIKE %s
        """, (f"%{keyword}%",))
        result = cur.fetchall()
        cur.close()
        return result

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()
