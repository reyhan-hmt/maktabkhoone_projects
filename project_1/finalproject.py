import mysql.connector
import requests
import re
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
html_content = response.text

def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text(strip=True)



pattern = re.compile(
    r'<h3 class="country-name">(?P<name>.*?)</h3>.*?'
    r'<span class="country-capital">(?P<capital>.*?)</span>.*?'
    r'<span class="country-population">(?P<population>[\d,]+)</span>.*?'
    r'<span class="country-area">(?P<area>[\d,\.]+)</span>',
    re.DOTALL
)

countries = []
for match in pattern.finditer(html_content):
    name = clean_html(match.group('name').strip())  
    capital = clean_html(match.group('capital').strip())  
    population = int(match.group('population').replace(',', ''))
    area = float(match.group('area').replace(',', ''))
    countries.append((name, capital, population, area))

db_config = {
    'user': 'root',     
    'password': '',  
    'host': '127.0.0.1',
    'database': 'world_data'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            capital VARCHAR(255),
            population BIGINT,
            area FLOAT
        )
    """)

    insert_query = """
        INSERT INTO countries (name, capital, population, area)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(insert_query, countries)
    conn.commit()

    print(f"{cursor.rowcount} records inserted into the database.")

finally:
    cursor.close()
    conn.close()

average_density = 50  
for country in countries:
    estimated_area = country[2] / average_density
    print(f"Estimated area for {country[0]}is {estimated_area:.2f} km²")
