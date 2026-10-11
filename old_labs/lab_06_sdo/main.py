import sqlite3

# функция для создания тестовой бд
def setup_test_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем обычные таблицы
    cursor.execute("CREATE TABLE IF NOT EXISTS Book (id INTEGER PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Member (id INTEGER PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Author (id INTEGER PRIMARY KEY)")
    
    # Создаем правильную таблицу связки
    cursor.execute("CREATE TABLE IF NOT EXISTS Book_Member (book_id INTEGER, member_id INTEGER)")
    
    # Создаем таблицу с подчеркиванием, но не являющуюся связкой
    cursor.execute("CREATE TABLE IF NOT EXISTS Some_Table (id INTEGER PRIMARY KEY)")
    
    conn.commit()
    conn.close()

def get_junction_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем названия всех таблиц в базе данных из системной таблицы sqlite_master
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    results = cursor.fetchall()
    
    all_tables = []
    for row in results:
        all_tables.append(row[0])
        
    junction_tables = []
    
    # Ищем таблицы связки среди всех таблиц
    for table in all_tables:
        if '_' in table:
            parts = table.split('_')
            
            # Проверяем, что частей ровно две, и обе существуют как отдельные таблицы
            if len(parts) == 2:
                if parts[0] in all_tables and parts[1] in all_tables:
                    junction_tables.append(table)
                    
    conn.close()
    
    return junction_tables

# Тестируем работу программы
db_file = 'librarydb-sqlite.db'

setup_test_db(db_file)

result = get_junction_tables(db_file)
print("Найденные таблицы связки:", result)