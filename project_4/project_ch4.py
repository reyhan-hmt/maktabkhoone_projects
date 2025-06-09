import mysql.connector
import re
import requests


url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

    country_pattern = r'<h3 class="country-name">([^<]+)</h3>'
    capital_pattern = r'<span class="country-capital">([^<]+)</span>'
    population_pattern = r'<span class="country-population">([\d,]+)</span>'
    area_pattern = r'<span class="country-area">([\d,]+)</span>'

    countries = re.findall(country_pattern, html_content)
    capitals = re.findall(capital_pattern, html_content)
    populations = re.findall(population_pattern, html_content)
    areas = re.findall(area_pattern, html_content)

    countries = [country.strip() for country in countries]
    capitals = [capital.strip() for capital in capitals]
    populations = [population.replace(",", "") for population in populations]
    areas = [area.replace(",", "") for area in areas]

    data = []
    for i in range(min(20, len(countries))): 
        data.append((countries[i], capitals[i], populations[i], areas[i]))
   

    cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='countries.info')
                                

    cursor = cnx.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            name VARCHAR(255),
            capital VARCHAR(255),
            population BIGINT,
            area FLOAT
        )
    ''')

    cursor.executemany('''
        INSERT INTO countries (name, capital, population, area)
        VALUES (%s, %s, %s, %s)
    ''', data)


    cnx.commit()
    cursor.close()
    cnx.close()


    print("Data saved to the  database successfully!")
else:
    print("Error fetching the page.")






   