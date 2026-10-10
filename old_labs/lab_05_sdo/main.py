import urllib.request
import json
import os
from bs4 import BeautifulSoup

def get_schedule_json_path(url):
    # Читаем HTML и игнорируем битые символы
    response = urllib.request.urlopen(url)
    html_content = response.read().decode('windows-1251', errors='ignore')
    
    # Пытаемся починить сломанный HTML перед парсингом
    html_content = html_content.replace(";<tr", "> <tr")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Структура для сбора абсолютно всех данных
    schedule_data = {
        "all_page_text": soup.get_text(separator=' | ', strip=True),
        "all_links": [],
        "all_table_rows": []
    }
    
    # Вытаскиваем текст из всех ссылок
    for a_tag in soup.find_all('a'):
        schedule_data["all_links"].append(a_tag.getText(separator=' ', strip=True))
        
    # Вытаскиваем все строки из всех таблиц
    for row in soup.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.getText(separator=' ', strip=True))
        
        if row_data:
            schedule_data["all_table_rows"].append(row_data)
            
    file_path = 'schedule.json'
    
    # Сохраняем в файл
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(schedule_data, json_file, ensure_ascii=False, indent=4)
        
    return os.path.abspath(file_path)

target_url = "https://schedule.siurgtu.ru/uTT.php"
result_path = get_schedule_json_path(target_url)
print("Файл успешно создан по пути:", result_path)