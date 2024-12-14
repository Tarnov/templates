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
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        content = soup.get_text(separator='\n')  # Добавление разделителя для улучшения читаемости
        save_to_database(title, content)
        print(f"Сохранено: {title}")
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")

# Основная функция
def main():
    print("Запуск программы WebScraper...")
    create_database()
    urls = [
        'https://example.com',
        'https://another-example.com'
    ]
    for url in urls:
        parse_website(url)
    print("Парсинг завершен.")

if __name__ == '__main__':
    main()

