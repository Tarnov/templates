import requests
from bs4 import BeautifulSoup
import sqlite3

# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('knowledge_base.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для сохранения данных в базу данных
def save_to_database(title, content):
    conn = sqlite3.connect('knowledge_base.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()

# Функция для парсинга сайта и извлечения данных
def parse_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        content = soup.get_text()
        save_to_database(title, content)
        print(f"Сохранено: {title}")
    else:
        print(f"Ошибка при загрузке страницы: {url}")

# Основная функция
def main():
    create_database()
    urls = [
        'https://example.com',
        'https://another-example.com'
    ]
    for url in urls:
        parse_website(url)

if __name__ == '__main__':
    main()
