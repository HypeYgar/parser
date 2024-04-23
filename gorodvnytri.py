import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def get_last_page_number_from_file(filename):
    """Функция для чтения последнего значения страницы из файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                return int(last_line)
    except FileNotFoundError:
        return None
class ELibraryScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def open_proxy_site(self):
        """Открыть прокси-сайт и перейти на гугл через croxyproxy."""
        self.driver.get("https://www.croxyproxy.net/_ru/")

            # Ждем появления ссылки "Гугл" на странице прокси с таймаутом 15 секунд
        google_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="quickLinks"]/a[2]')))
        google_link.click()

    def handle_consent_dialog(self):
        """Обработать диалог согласия (если присутствует)."""
        try:
            consent_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="L2AGLb"]')))
            consent_button.click()
            time.sleep(5)
        except:
            pass

    def search_elibrary(self):
        """Выполнить поиск elibrary.ru и перейти на сайт."""
        search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="APjFqb"]')))
        search_box.send_keys("https://elibrary.ru")
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
        # Переход на страницу elibrary.ru
        elibrary_link = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3')))
        elibrary_link.click()

    def login_to_elibrary(self, username, password):
        """Авторизация на сайте elibrary.ru."""
        login_field = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]')))
        login_field.click()
        login_field.send_keys(username)
        password_field = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.click()
        password_field.send_keys(password)
        login_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="win_login"]/table[1]/tbody/tr[9]/td/div[2]')))
        login_button.click()
        # Нажать на ссылку для поиска по ГОРОДУ
        search_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="win_goto"]/table[1]/tbody/tr[6]/td[2]/a')))
        search_button.click()
        time.sleep(3)

    def search_by_GOROD(self, city_list_file):
        """Выполнить поиск по названиям городов и сохранить информацию в файл."""
        with open(city_list_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Читаем строки из файла
            for city_name in lines:
                city_name = city_name.strip()  # Удаляем лишние пробелы и символы новой строки

                try:
                    # Найти поле ввода и ввести название города
                    input_field = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[1]/tbody/tr/td[2]/input")))
                    input_field.clear()
                    input_field.send_keys(city_name)

                    # Нажать на вторую кнопку поиска
                    search_button2 = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[3]/tbody/tr/td[6]/a')))
                    search_button2.click()

                    time.sleep(3)  # Небольшая задержка для загрузки страницы после поиска

                    # Нажать на ссылку для перехода на новую страницу
                    link_to_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[4]/tbody/tr[2]/td[2]/font/a')))
                    link_to_click.click()

                    time.sleep(3)
                    # Найти и сохранить нужные элементы в файл

                    with open('city_info.txt', 'a', encoding='utf-8') as info_file:
                        info_file.write(f"Город: {city_name}\n")

                        # Проверяем и сохраняем полное название
                        full_name_element = None
                        try:
                            full_name_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[1]/tbody/tr/td[2]/font/b')))
                        except:
                            pass

                        if full_name_element:
                            full_name = full_name_element.text.strip()
                            info_file.write(f"Полное название: {full_name}\n")
                            print(full_name)

                        # Проверяем и сохраняем название на английском
                        english_name_element = None
                        try:
                            english_name_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                   '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[1]/td[2]/font')))
                        except:
                            pass

                        if english_name_element:
                            english_name = english_name_element.text.strip()
                            info_file.write(f"Название на английском: {english_name}\n")
                            print(english_name)

                        # Проверяем и сохраняем сокращение
                        abbreviation_element = None
                        try:
                            abbreviation_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                   '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[2]/tbody/tr[2]/td[2]/font')))
                        except:
                            pass

                        if abbreviation_element:
                            abbreviation = abbreviation_element.text.strip()
                            info_file.write(f"Сокращение: {abbreviation}\n")
                            print(abbreviation)

                        # Проверяем и сохраняем сокращение на английском
                        english_abbreviation_element = None
                        try:
                            english_abbreviation_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                                           '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[4]/font')))
                        except:
                            pass

                        if english_abbreviation_element:
                            english_abbreviation = english_abbreviation_element.text.strip()
                            info_file.write(f"Сокращение на английском: {english_abbreviation}\n")
                            print(english_abbreviation)

                        # Проверяем и сохраняем страну
                        country_element = None
                        try:
                            country_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                              '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/font/a')))
                        except:
                            pass

                        if country_element:
                            country = country_element.text.strip()
                            info_file.write(f"Страна: {country}\n")
                            print(country)

                        # Проверяем и сохраняем город
                        city_element = None
                        try:
                            city_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                           '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/font/a')))
                        except:
                            pass

                        if city_element:
                            city = city_element.text.strip()
                            info_file.write(f"Город: {city}\n")
                            print(city)

                        # Проверяем и сохраняем почтовый адрес
                        address_element = None
                        try:
                            address_element = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                              '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[4]/tbody/tr[1]/td[2]/font')))
                        except:
                            pass

                        if address_element:
                            address = address_element.text.strip()
                            info_file.write(f"Почтовый адрес: {address}\n\n")
                            print(address)

                            # Нажать на ссылку для перехода на новую страницу
                        link_to_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[6]/td/div/table/tbody/tr/td/table/tbody/tr[6]/td[1]/a')))
                        link_to_click.click()

                except Exception as e:
                    print(f"Ошибка при обработке города '{city_name}': {e}")

    def quit(self):
        """Закрыть браузер после завершения."""
        self.driver.quit()
def main_script():
    while True:
        try:
            # Ваш основной код парсинга здесь
            scraper = ELibraryScraper()
            scraper.open_proxy_site()
            scraper.handle_consent_dialog()
            scraper.search_elibrary()
            scraper.login_to_elibrary(username="Evanepon", password="LegoEva210877")
            scraper.search_by_GOROD("kaif.txt")
        except Exception as e:
            error_message = str(e)

# Вызов функции для выполнения основного скрипта
if __name__ == "__main__":
    main_script()
