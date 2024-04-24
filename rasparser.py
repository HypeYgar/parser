import re


def extract_organization_names(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = infile.read()

        # Используем регулярное выражение для извлечения содержимого между тегами <a></a>
        organization_names = re.findall(r'<a[^>]*>(.*?)</a>', data, re.DOTALL)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for name in organization_names:
                outfile.write(name.strip() + '\n')


# Пример использования
input_filename = 'vxoddannix.txt'
output_filename = 'vixoddannix.txt'

extract_organization_names(input_filename, output_filename)
