import json
import csv
import os

os.makedirs("data", exist_ok=True)

JSON_FILE = "data/data.json"
CSV_FILE = "data/data.csv"

def load_json():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_json(data_list):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)

def export_csv(data_list):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        if not data_list:
            return
        
        writer = csv.writer(file)
        writer.writerow(["ФИО", "Возраст", "Вид спорта", "Результат"])
        
        for item in data_list:
            writer.writerow([item["full_name"], item["age"], item["sport_type"], item["result"]])