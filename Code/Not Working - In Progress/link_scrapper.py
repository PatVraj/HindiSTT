import time
import os
import random
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

@contextmanager
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--enable-javascript")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.close()
        os.system("pkill Chrome")
        driver.quit()

def scrape_text_from_url(url):
    with create_driver() as driver:
        try:
            driver.set_page_load_timeout(30)  # Set a timeout of 30 seconds
            driver.get(url)
            time.sleep(3)  # Let the page load
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            article = soup.find('article', class_='articleBody main_article_content')
            if not article:
                article = soup.find('div', class_='article-content')
            if not article:
                article = soup.find('div', class_='content')
            if not article:
                return "No article content found."
            paragraphs = article.find_all('p')
            if not paragraphs:
                return "No paragraphs found in the article."
            text = '\n'.join([p.get_text() for p in paragraphs])
            if len(text) < 100:
                print(f"Insufficient content scraped from {url}")
                return "Insufficient content scraped from the article."
            return text
        except TimeoutException:
            print(f"Timeout occurred while loading {url}")
            return "Timeout occurred while loading the page."
        except NoSuchElementException:
            print(f"Expected elements not found on the page {url}")
            return "Unable to locate the article content on the page."
        except Exception as e:
            print(f"Error occurred while scraping {url}: {str(e)}")
            return "Error occurred while scraping the article."

def save_to_file(entries, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for date, url in entries:
            text = scrape_text_from_url(url)
            file.write(f"Date: {date}\n")
            file.write(f"URL: {url}\n")
            file.write(text + '\n\n')
            time.sleep(random.uniform(1, 3))  # Add a random delay between each URL scrape

def parse_file(filename):
    dates_links = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            try:
                date = lines[i].strip().split(': ')[1]
                link = lines[i + 1].strip().split(': ')[1]
                dates_links.append((date, link))
            except IndexError:
                pass
    return dates_links

# File paths
input_file_path = 'speech_links.txt'
output_file_path = 'Modi_Speeches.txt'

# Parse input file and save scraped text to file
parsed_data = parse_file(input_file_path)
save_to_file(parsed_data, output_file_path)