import psycopg2
from config import DB_CONFIG


def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            website VARCHAR(255)
        )
    """)

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


if __name__ == "__main__":
    create_tables()

