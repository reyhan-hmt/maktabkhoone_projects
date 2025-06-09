import re
import requests

url = "https://divar.ir/s/tehran"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
    pattern = r'<span[^>]*>([^<]*توافقی[^<]*)</span>'
    matches = re.findall(pattern, html_content, re.DOTALL)

    if matches:
        print("Result:")
        for match in matches:
            print(match)  
    else:
        print("No result found")
else:
    print("Error fetching the page")
