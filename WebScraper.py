import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
import logging
from concurrent.futures import ThreadPoolExecutor
import configparser

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')

db_config = config['Database']
dbname = db_config['dbname']
user = db_config['user']
password = db_config['password']
host = db_config['host']
port = db_config['port']

# Функция для создания базы данных и таблицы
def create_database():
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
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
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (title, content) VALUES (%s, %s)', (title, content))
    conn.commit()
    conn.close()

# Функция для парсинга сайта и извлечения данных
def parse_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        content = soup.get_text(separator='\n')  # Добавление разделителя для улучшения читаемости
        save_to_database(title, content)
        logging.info(f"Сохранено: {title}")
    except requests.RequestException as e:
        logging.error(f"Ошибка при загрузке страницы {url}: {e}")

# Основная функция
def main():
    logging.info("Запуск программы WebScraper...")
    create_database()

    # Чтение URL-адресов из файла
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    # Удаление символов новой строки
    urls = [url.strip() for url in urls]

    # Использование ThreadPoolExecutor для параллельного выполнения
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(parse_website, urls)

    logging.info("Парсинг завершен.")

if __name__ == '__main__':
    main()
