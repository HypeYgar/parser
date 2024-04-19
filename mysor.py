import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get("https://www.croxyproxy.net/_ru/")

try:
    ##переход с помощью croxyproxy на гугл
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="quickLinks"]/a[2]'))
    )
    element.click()
    time.sleep(5)
    ##гугл подтвердить если есть этот XPATH то нажать если нет то пропускать
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="L2AGLb"]'))
        )
        element.click()
        time.sleep(5)
    except:
        pass  # Если элемент не найден, просто пропустите этот шаг

    # Ввод текста в полеГУГЛА И НАЖАТЬ ПОИСК
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="APjFqb"]'))
    )
    element.send_keys("https://elibrary.ru")
    element.send_keys(Keys.ENTER)
    ## НАЖАТЬ НА ССЫЛКУ ЕЛАЙБРЕРИ
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3'))
    )
    element.click()

    ##РЕГИСТРАЦИЯ
    ##ЛОГИН
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login"]'))
    )
    element.click()
    element.send_keys("Evanepon")
    ##PASSWORD
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
    )
    element.click()
    element.send_keys("LegoEva210877")


    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="win_login"]/table[1]/tbody/tr[9]/td/div[2]'))
    )
    element.click()
##нажать поиск по автору
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="win_goto"]/table[1]/tbody/tr[5]/td[2]/a'))
    )
    element.click()
    ##вод в поле фамилия
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="surname"]'))
    )
    element.clear()
    ##ПОИСК АВТОРА
    with open('authors.txt', 'r', encoding='utf-8') as file:

        lines = file.readlines()
        for line in lines:

            ##вод в поле фамилия
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="surname"]'))
            )
            element.clear()
            element.send_keys(line.strip())

            # Нажатие на кнопку поиск
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="show_param"]/table[6]/tbody/tr[2]/td[6]/div'))
            )
            element.click()

            # на список публикаций
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[4]/td[4]/div/a[1]'))
            )
            element.click()
            print("neq2wn")
            try:
                print("nedwn")
                # Проверкаw значений в таблице

                for i in range(4, 24):
                    xpath = f'/html/body/div[5]/table/tbody/tr/td/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[{i}]/td[3]'
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        value = element.text.strip()
                        if value and float(value) > 0:
                            link = element.get_attribute('href')
                            with open('links.txt', 'a', encoding='utf-8') as file:
                                file.write(link + '\n')
                    except Exception as e:
                        print(f"Error processing value: {e}")
                try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 '//*[@id="pages"]/table/tbody/tr/td[7]/a'))
                        )
                        element.click()
                        time.sleep(5)
                except:
                    pass

            except:
                pass

finally:
    driver.quit()



########################



