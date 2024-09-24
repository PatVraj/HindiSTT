import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import hashlib
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create a folder to save the speeches if it doesn't exist
modi_speeches_dir = os.path.join(script_dir, 'Modi_Speeches')
if not os.path.exists(modi_speeches_dir):
    os.makedirs(modi_speeches_dir)

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
#options.add_argument("--headless") # Uncomment this line to run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Function to read speech links from the text file
def read_speech_links(file_path):
    # Print current working directory for debugging
    logging.info(f"Current working directory: {os.getcwd()}")

    # Check if the file exists
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        speech_links = []
        current_speech = {}
        for line in lines:
            if line.startswith("Date:"):
                if current_speech:
                    speech_links.append(current_speech)
                current_speech = {}
                current_speech['date'] = line.replace("Date: ", "").strip()
            elif line.startswith("Link:"):
                current_speech['link'] = line.replace("Link: ", "").strip()

        if current_speech:
            speech_links.append(current_speech)

    return speech_links

# Function to scrape the speech text from a given URL
def scrape_speech_text(url):
    driver.get(url)
    try:
        # Wait for the article to load, #ISSUES
        #time.sleep(5)
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'articleBody main_article_content')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article = soup.find('article', class_='articleBody main_article_content')
        if article:
            text = '\n'.join([p.get_text() for p in article.find_all('p')])
            return text
        else:
            logging.error(f"Article not found for URL: {url}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred while scraping {url}: {e}")
        return None

# Read the speech links from the file
speech_links_file = os.path.join(script_dir, 'speech_links.txt')
logging.info(f"Reading speech links from {speech_links_file}")
speech_links = read_speech_links(speech_links_file)

# Counter to handle multiple speeches on the same date
date_counter = {}

# Scrape and save each speech
for speech in speech_links:
    date = speech['date']
    url = speech['link']

    # Format the date string in m d Y format
    date_str = datetime.strptime(date, '%B %d, %Y').strftime('%m %d %Y')

    # Use a counter to differentiate multiple speeches on the same date
    if date_str not in date_counter:
        date_counter[date_str] = 1
    else:
        date_counter[date_str] += 1

    # Generate a unique filename using the date and a hash of the URL
    url_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    filename = os.path.join(modi_speeches_dir, f"{date_str}_{date_counter[date_str]}_{url_hash}.txt")

    # Scrape the speech text
    logging.info(f"Scraping speech from {url}")
    text = scrape_speech_text(url)

    if text:
        # Save the text to a file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        logging.info(f"Saved speech to {filename}")

# Close the WebDriver
driver.quit()