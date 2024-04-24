import asyncio
import time
import traceback
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from telegram import Bot

def send_telegram_message(bot_token, chat_id, message):
    """Функция для отправки сообщения в Telegram."""
    try:
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

def send_telegram_document(bot_token, chat_id, document_path, caption=""):
    """Функция для отправки документа в Telegram."""
    try:
        bot = Bot(token=bot_token)
        asyncio.run(bot.send_document(chat_id=chat_id, document=open(document_path, 'rb'), caption=caption))
    except Exception as e:
        print(f"Ошибка при отправке документа в Telegram: {e}")

class ELibraryScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def open_proxy_site(self):
        """Открыть прокси-сайт и перейти на гугл через croxyproxy."""
        self.driver.get("https://www.croxyproxy.net/_ru/")
        google_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="quickLinks"]/a[2]')))
        google_link.click()

    def handle_consent_dialog(self):
        """Обработать диалог согласия (если присутствует)."""
        try:
            consent_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="L2AGLb"]')))
            consent_button.click()
            time.sleep(5)
        except TimeoutException:
            pass

    def search_elibrary(self):
        """Выполнить поиск elibrary.ru и перейти на сайт."""
        search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="APjFqb"]')))
        search_box.send_keys("https://elibrary.ru")
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
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
        search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="win_goto"]/table[1]/tbody/tr[6]/td[2]/a')))
        search_button.click()
        time.sleep(3)

    def search_by_GOROD(self, city_list_file):
        """Выполнить поиск по названиям городов и сохранить информацию в файл."""
        last_processed_line_file = 'last_processed_line.txt'

        last_processed_line = 0
        try:
            with open(last_processed_line_file, 'r') as f:
                last_processed_line = int(f.read().strip())
        except FileNotFoundError:
            pass
        except ValueError:
            print("Ошибка чтения файла last_processed_line.txt. Начинаем с начала списка.")

        with open(city_list_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i in range(last_processed_line, len(lines)):
                city_name = lines[i].strip()

                try:
                    input_field = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[1]/tbody/tr/td[2]/input")))
                    input_field.clear()
                    input_field.send_keys(city_name)

                    search_button2 = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[3]/tbody/tr/td[6]/a')))
                    search_button2.click()

                    time.sleep(3)

                    link_to_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[4]/tbody/tr[2]/td[2]/font/a')))
                    link_to_click.click()

                    time.sleep(3)

                    with open('city_info.txt', 'a', encoding='utf-8') as info_file:
                        info_file.write(f"------------------------\n")
                        info_file.write(f"Город: {city_name}\n")
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
                        info_file.write(f"------------------------\n")
                        # Сохранить номер строки, с которой начнется следующий запуск
                        with open(last_processed_line_file, 'w') as f:
                            f.write(str(i + 1))
                        link_to_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[6]/td/div/table/tbody/tr/td/table/tbody/tr[6]/td[1]/a')))
                        link_to_click.click()

                except Exception as e:
                    print(f"Ошибка при обработке города '{city_name}': {e}")
                    send_telegram_document("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457",
                                           "city_info.txt", f"Произошла ошибка:")

    def quit(self):
        """Закрыть браузер после завершения."""
        self.driver.quit()

def main_script():
    while True:
        try:
            send_telegram_document("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", "city_info.txt", f"браузер включился: ")
            scraper = ELibraryScraper()
            scraper.open_proxy_site()
            scraper.handle_consent_dialog()
            scraper.search_elibrary()
            scraper.login_to_elibrary(username="Evanepon", password="LegoEva210877")
            scraper.search_by_GOROD("kaif.txt")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            send_telegram_document("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", "city_info.txt", f"Произошла ошибка:")
        finally:
            scraper.quit()
            send_telegram_document("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", "city_info.txt", f"браузер выключился: ")


if __name__ == "__main__":
    main_script()

