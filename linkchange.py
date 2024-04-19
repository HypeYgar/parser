import re

def extract_links_from_file(file_path):
    links = []

    # Открываем файл для чтения
    with open(file_path, 'r', encoding='utf-8') as file:
        # Читаем содержимое файла построчно
        for line in file:
            # Используем регулярное выражение для поиска всех ссылок в строке
            found_links = re.findall(r'href="([^"]+)"', line)

            # Добавляем найденные ссылки в список
            links.extend(found_links)

    return links

# Укажите путь к вашему файлу
file_path = 'links_GOROD.txt'

# Извлечение ссылок из файла
links = extract_links_from_file(file_path)

# Укажите путь к новому файлу, в который нужно сохранить ссылки
output_file = 'extracted_links.txt'

# Сохранение извлеченных ссылок в новый файл
extract_links_from_file(links, output_file)

print(f"Ссылки сохранены в файл: {output_file}")
