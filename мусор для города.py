import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

    def search_by_GOROD(self, author_list_file):
        """Выполнить поиск и сохранить XPATH в файл по городу."""
        # Нажать поиск по ГОРОДУ
        search_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="win_goto"]/table[1]/tbody/tr[6]/td[2]/a')))
        search_button.click()
        time.sleep(3)

        # Находим поле ввода
        input_field = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[1]/tbody/tr/td[2]/input")))
        input_field.click()
        input_field.clear()

        # Нажать на вторую кнопку поиска
        search_button2 = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[3]/tbody/tr/td[6]/a')))
        search_button2.click()

        with open(author_list_file, 'a', encoding='utf-8') as file:
            page_number = 1
            while True:
                for i in range(2, 22):
                    xpath = f'/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[4]/tbody/tr[{i}]/td[2]/font/a'
                    try:
                        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                        element_code = element.get_attribute('outerHTML')
                        file.write(element_code + '\n')
                    except Exception as e:
                        print(f"Error: {e}")

                # Переход на следующую страницу
                try:
                    page_number = 38
                    script = f'goto_page({page_number})'
                    self.driver.execute_script(script)

                    # Если нужно дать странице время загрузиться, добавьте задержку
                    print("edfofke")
                    time.sleep(33) # Дайте странице время загрузиться
                    page_number += 1

                    # Проверяем, прошло ли 20 страниц (и делится ли номер страницы на 20 без остатка)
                    if page_number % 10 == 0:
                        print("Переключение на следующую 20 страниц. Подождите 30 секунд...")
                        time.sleep(30)  # Задержка в 30 секунд

                except Exception as e:
                    print(f"No more pages to load: {e}")
                    break  # Выход из цикла, если больше нет страниц

        print(f"Search completed. Saved results to {author_list_file}")

    def quit(self):
        """Закрыть браузер после завершения."""
        self.driver.quit()

if __name__ == "__main__":
    scraper = ELibraryScraper()
    try:
        scraper.open_proxy_site()

        # Обработать диалог согласия (если присутствует)
        scraper.handle_consent_dialog()

        # Выполнить поиск elibrary.ru и перейти на сайт
        scraper.search_elibrary()

        # Авторизация на сайте elibrary.ru
        scraper.login_to_elibrary(username="Evanepon", password="LegoEva210877")
        scraper.search_by_GOROD("links_GOROD.txt")

    finally:
        # Закрыть браузер после завершения
        scraper.quit()
