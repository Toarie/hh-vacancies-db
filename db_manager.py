import psycopg2
from config import DB_CONFIG


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def get_companies_and_vacancies_count(self):
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
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM vacancies 
            WHERE title ILIKE %s
        """, (f"%{keyword}%",))
        result = cur.fetchall()
        cur.close()
        return result

    def close(self):
        self.conn.close()

