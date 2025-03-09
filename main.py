from bs4 import BeautifulSoup
import lxml
import time
import requests
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib3.filepost import writer
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

while True:
    url_town = "https://example.com/local-news"  
    url_country = "https://example.com/national-news"  
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "text/html",
    }
    
    tg_token = "YOUR_BOT_TOKEN"  
    tg_chat_id = "YOUR_CHAT_ID" 

    def tg_send_message(photo_url, title, text, url):
        telegram_url = f"https://api.telegram.org/bot{tg_token}/sendPhoto"
        params = {
            "chat_id": tg_chat_id,
            "photo": photo_url,
            "caption": f"<b>{title}</b>\n\n{text}\n\n🔗 <a href='{url}'>Link to the news</a>",
            "parse_mode": "HTML"
        }
        requests.get(telegram_url, params=params)

    def click_buttons():
        try:
            accept_all_button = WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.CLASS_NAME, "cmp-button_button"))
            )
            accept_all_button.click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(3)
        try:
            reject_button = WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.CLASS_NAME, "cmp-intro_rejectAll"))
            )
            reject_button.click()
        except Exception as e:
            print(f"Error: {e}")

    def save_names(list_of_names):
        with open("names_list.csv", "w", encoding="utf8", newline='') as file:
            wrt = csv.writer(file)
            for items in list_of_names:
                wrt.writerow([items])  # Записываем каждое имя в новую строку

    def searcher():
        try:
            with open("names_list.csv", "r", encoding="utf8") as file:
                reader = csv.reader(file)
                list_data = [row[0] for row in reader]  # Читаем только первое значение из каждой строки
        except:
            list_data = []
        return list_data

    list_data = searcher()

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Запускаем браузер в полном экране
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Скрываем автоматизацию
    chrome_options.add_argument("--headless")  # Запуск браузера в фоновом режиме
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Запуск драйвера

    driver.get(url_town)

    click_buttons()

    url_town_html = driver.page_source
    key_word = re.compile("itemBox")
    soup = BeautifulSoup(url_town_html, features="lxml")
    news_cards_el_bot = soup.find_all("a", class_=key_word)
    news_cards_el_top = soup.find_all("a", class_="mediumNewsBox lpsItem")

    for item in news_cards_el_top + news_cards_el_bot:
        try:
            mini_name = item.find("h3", class_="title").text
            if mini_name not in list_data:
                img_code = item.find("img").get("src")
                img = f"https:{img_code}"
                link = item.get("href")
                driver.get(link)
                link_html = driver.page_source
                title_word = re.compile("mainTitle")
                new_soup = BeautifulSoup(link_html, features="lxml")
                name = new_soup.find("h1", class_="mainTitle").text.strip()
                data = new_soup.find("div", id="lead").text
                tg_send_message(img, name + " #LocalNews", data, link)
                list_data.append(mini_name)  # Добавляем новое имя в список
        except:
            pass

    driver.get(url_country)
    url_country_html = driver.page_source
    soup = BeautifulSoup(url_country_html, features="lxml")
    all_country_news = soup.find_all("div", class_="listItem listItemSolr itarticle")

    for info in all_country_news:
        try:
            mini_name = info.find("h3", class_="itemTitle").text.strip()
            if mini_name not in list_data:
                img_code = info.find("img").get("src")
                img = f"https:{img_code}"
                name = mini_name
                data = info.find("div", class_="itemLead hyphenate").text.strip()
                link = info.find("a").get("href")
                tg_send_message(img, name + " #NationalNews", data, link)
                list_data.append(mini_name)  # Добавляем новое имя в список
        except:
            pass

    driver.quit()

    save_names(list_data)
    time.sleep(900)
