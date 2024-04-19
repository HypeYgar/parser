import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re


def extract_links_from_html(file_path):
    # Открываем файл
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Используем регулярные выражения, чтобы найти все значения href
    links = re.findall(r'href=\"(.*?)\"', content)

    # Записываем ссылки обратно в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\\n')
class ELibraryScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def open_proxy_site(self):
        """Открыть прокси-сайт и перейти на гугл через croxyproxy."""
        self.driver.get("https://www.croxyproxy.net/_ru/")
        # Ждем появления ссылки "Гугл" на странице прокси
        google_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="quickLinks"]/a[2]')))
        google_link.click()
        time.sleep(5)

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
        elibrary_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3')))
        elibrary_link.click()

    def login_to_elibrary(self, username, password):
        """Авторизация на сайте elibrary.ru."""
        login_field = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]')))
        login_field.click()
        login_field.send_keys(username)

        password_field = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.click()
        password_field.send_keys(password)

        login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="win_login"]/table[1]/tbody/tr[9]/td/div[2]')))
        login_button.click()


    def search_by_author(self, author_list_file):
        ##нажать поиск по автору
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="win_goto"]/table[1]/tbody/tr[5]/td[2]/a'))
        )
        element.click()

        with open(author_list_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                author_name = line.strip()
                try:
                    # ввод имени
                    author_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="surname"]')))
                    author_input.clear()
                    author_input.send_keys(author_name)

                    # кнопка поиск
                    search_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="show_param"]/table[6]/tbody/tr[2]/td[6]/div')))
                    search_button.click()

                    # клик на публикации
                    first_publication_link = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                         '/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[4]/td[4]/div/a[1]')))
                    first_publication_link.click()

                    # Process publication values
                    for i in range(4, 24):
                        xpath = f'/html/body/div[5]/table/tbody/tr/td/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[{i}]/td[3]'
                        try:
                            element = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, xpath))
                            )
                            value = element.text
                            print(value)
                            if float(value) > 0:
                                link = element.get_attribute('outerHTML')
                                print((link))
                                with open('links.txt', 'a', encoding='utf-8') as file:
                                    if link is not None:

                                        file.write(link + '\\n')
                        except:
                            pass
                    # пагинация
                    try:
                        next_page_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="pages"]/table/tbody/tr/td[7]/a')))
                        next_page_button.click()
                        time.sleep(5)
                    except:
                        pass

                except Exception as e:
                    print(f"Error processing author '{author_name}': {e}")



    def quit(self):
        """Закрыть браузер после завершения."""
        self.driver.quit()

if __name__ == "__main__":
    scraper = ELibraryScraper()
    try:
        # Открыть прокси-сайт и перейти на гугл через croxyproxy
        scraper.open_proxy_site()

        # Обработать диалог согласия (если присутствует)
        scraper.handle_consent_dialog()

        # Выполнить поиск elibrary.ru и перейти на сайт
        scraper.search_elibrary()

        # Авторизация на сайте elibrary.ru
        scraper.login_to_elibrary(username="Evanepon", password="LegoEva210877")

        # Выполнить поиск авторов
        scraper.search_by_author(author_list_file="authors.txt")

    finally:
        # Закрыть браузер после завершения
        scraper.quit()
