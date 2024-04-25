import asyncio
import time
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from telegram import Bot
import pyautogui
from PIL import Image

machine_num=1
def count_phrase_occurrences(file_path, phrase):
    count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if phrase in line:
                count += 1
    return count

async def send_telegram_message(bot_token, chat_id, message):
    """Функция для отправки сообщения в Telegram."""
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

async def send_telegram_document(bot_token, chat_id, document_path, caption=""):
    """Функция для отправки документа в Telegram."""
    try:
        bot = Bot(token=bot_token)
        await bot.send_document(chat_id=chat_id, document=open(document_path, 'rb'), caption=caption)
    except Exception as e:
        print(f"Ошибка при отправке документа в Telegram: {e}")

async def send_telegram_scrin(bot_token, chat_id, image_path, caption=""):
    """Функция для отправки изображения (скриншота) в Telegram."""
    try:
        bot = Bot(token=bot_token)
        image = Image.open(image_path)
        bio = BytesIO()
        image.save(bio, format='PNG')
        bio.seek(0)
        await bot.send_photo(chat_id=chat_id, photo=bio, caption=caption)
    except Exception as e:
        print(f"Ошибка при отправке изображения в Telegram: {e}")

class ELibraryScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    async def open_proxy_site(self):
        """Открыть прокси-сайт и перейти на гугл через croxyproxy."""
        self.driver.get("https://www.croxyproxy.net/_ru/")
        google_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="quickLinks"]/a[2]')))
        google_link.click()

    async def handle_consent_dialog(self):
        """Обработать диалог согласия (если присутствует)."""
        try:
            consent_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="L2AGLb"]')))
            consent_button.click()
            time.sleep(5)
        except TimeoutException:
            pass

    async def search_elibrary(self):
        """Выполнить поиск elibrary.ru и перейти на сайт."""
        search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="APjFqb"]')))
        search_box.send_keys("https://elibrary.ru")
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
        elibrary_link = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3')))
        elibrary_link.click()

    async def login_to_elibrary(self, username, password):
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

    async def search_by_GOROD(self, city_list_file):
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
                    if "Не найдено организаций" in self.driver.page_source:
                        print(f"Организации не найдены для города '{city_name}'")
                        with open('city_info_error.txt', 'a', encoding='utf-8') as info_file:
                            info_file.write(f"Организации не найдены для города '{city_name}'\n")
                            await send_telegram_document("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", "city_info_error.txt", f"Машина номер {machine_num}.нашел ошибку иди нахуй: ")
                        continue

                    time.sleep(3)

                    link_to_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                '/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table[4]/tbody/tr[2]/td[2]/font/a')))
                    link_to_click.click()

                    time.sleep(3)

                    with open('city_info.txt', 'a', encoding='utf-8') as info_file:
                        info_file.write(f"------------------------\n")
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
                        error_message = f"Машина номер {machine_num}. Скрин {full_name}"
                        screenshot_path = 'screenshot.png'
                        pyautogui.screenshot(screenshot_path)
                        await send_telegram_scrin("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4123199178", screenshot_path, error_message)
                        info_file.write(f"------------------------\n")
                        # Сохранить номер строки, с которой начнется следующий запуск
                        with open(last_processed_line_file, 'w') as f:
                            f.write(str(i + 1))
                        link_to_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[6]/td/div/table/tbody/tr/td/table/tbody/tr[6]/td[1]/a')))
                        link_to_click.click()

                except Exception as e:
                    break

    def quit(self):
        """Закрыть браузер после завершения."""
        self.driver.quit()

async def main_script_async():
    while True:
        try:
            await send_telegram_message("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", f"Машина номер {machine_num}.браузер включился")
            scraper = ELibraryScraper()
            await scraper.open_proxy_site()
            await scraper.handle_consent_dialog()
            await scraper.search_elibrary()
            await scraper.login_to_elibrary(username="Evanepon", password="LegoEva210877")
            await scraper.search_by_GOROD("kaif.txt")
        except Exception as e:
            error_message = f"Машина номер {machine_num}.Произошла ошибка: {e}"
            print(error_message)
            screenshot_path = 'screenshot.png'
            pyautogui.screenshot(screenshot_path)
            await send_telegram_scrin("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", screenshot_path, error_message)
        finally:
            scraper.quit()
            phrase_count = count_phrase_occurrences("city_info.txt", "Полное название:")
            await send_telegram_document("6988073004:AAGgq7YTG5BUF7P1BM_SFDtIRuLPiJc-8ZE", "-4109363457", "city_info.txt",
                                         f"Машина номер {machine_num}.браузер выключился.  Скок он спарсил: {phrase_count}")

def main():
    asyncio.run(main_script_async())

if __name__ == "__main__":
    main()
