import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql

# Функция для создания базы данных и таблицы
def create_database():
    conn = psycopg2.connect(
        dbname='your_db_name',
        user='your_db_user',
        password='your_db_password',
        host='your_db_host',
        port='your_db_port'
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для сохранения данных в базу данных
def save_to_database(title, content):
    conn = psycopg2.connect(
        dbname='your_db_name',
        user='your_db_user',
        password='your_db_password',
        host='your_db_host',
        port='your_db_port'
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (title, content) VALUES (%s, %s)', (title, content))
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

    # Чтение URL-адресов из файла
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    # Удаление символов новой строки
    urls = [url.strip() for url in urls]

    for url in urls:
        parse_website(url)
    print("Парсинг завершен.")

if __name__ == '__main__':
    main()
