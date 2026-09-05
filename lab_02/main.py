def add_track(playlist):
    title = input("Введите название композиции: ")
    artist = input("Введите исполнителя: ")
    genre = input("Введите жанр: ")
    
    duration = int(input("Введите продолжительность в секундах: "))
    if duration < 0:
        print("Ошибка: продолжительность не может быть отрицательной. Установлено 0.")
        duration = 0
        
    track = {
        "title": title,
        "artist": artist,
        "genre": genre,
        "duration": duration
    }
    playlist.append(track)
    print("Композиция успешно добавлена!")

def show_all(playlist):
    if not playlist:
        print("Плейлист пуст.")
        return
        
    for i, track in enumerate(playlist):
        print(f"{i + 1}. {track['artist']} - {track['title']} [{track['genre']}] ({track['duration']} сек.)")

def search_by_artist(playlist, target_artist):
    found = False
    for track in playlist:
        if track['artist'].lower() == target_artist.lower():
            print(f"- {track['title']} ({track['duration']} сек.)")
            found = True
            
    if not found:
        print("Композиции данного исполнителя не найдены.")

def filter_by_genre(playlist, target_genre):
    found = False
    for track in playlist:
        if track['genre'].lower() == target_genre.lower():
            print(f"- {track['artist']} - {track['title']}")
            found = True
            
    if not found:
        print("Композиции в данном жанре не найдены.")

def sort_by_duration(playlist):
    sorted_playlist = sorted(playlist, key=lambda x: x['duration'])
    print("Список отсортирован по возрастанию продолжительности:")
    show_all(sorted_playlist)

def show_statistics(playlist):
    if not playlist:
        print("Нет данных для статистики.")
        return

    total_duration = 0
    max_duration = playlist[0]['duration']
    longest_track = playlist[0]

    for track in playlist:
        total_duration += track['duration']
        if track['duration'] > max_duration:
            max_duration = track['duration']
            longest_track = track

    average_duration = total_duration / len(playlist)
    
    print(f"Средняя продолжительность трека: {average_duration:.1f} сек.")
    print(f"Самая длинная композиция: {longest_track['artist']} - {longest_track['title']} ({max_duration} сек.)")

def show_unique_artists(playlist):
    if not playlist:
        print("Плейлист пуст.")
        return
        
    unique_artists = set()
    for track in playlist:
        unique_artists.add(track['artist'])
        
    print("Уникальные исполнители в плейлисте:")
    for artist in unique_artists:
        print(f"- {artist}")


def main():
    playlist = []
    
    while True:
        print("\n===== МЕНЮ =====")
        print("1. Добавить композицию")
        print("2. Показать все композиции")
        print("3. Найти композиции исполнителя")
        print("4. Фильтрация по жанру")
        print("5. Сортировка по продолжительности")
        print("6. Статистика (средняя и максимальная длина)")
        print("7. Уникальные исполнители")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            add_track(playlist)
        elif choice == '2':
            show_all(playlist)
        elif choice == '3':
            artist_name = input("Введите имя исполнителя для поиска: ")
            search_by_artist(playlist, artist_name)
        elif choice == '4':
            genre_name = input("Введите жанр для фильтрации: ")
            filter_by_genre(playlist, genre_name)
        elif choice == '5':
            sort_by_duration(playlist)
        elif choice == '6':
            show_statistics(playlist)
        elif choice == '7':
            show_unique_artists(playlist)
        elif choice == '0':
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите номер из меню.")

if __name__ == "__main__":
    main()