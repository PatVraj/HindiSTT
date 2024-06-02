# %%
import os
import re
import time
import dateutil.parser
import random
import string
from datetime import datetime
from contextlib import closing
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

SPEECHES_DIR = "modi_speeches"

# %%
def scroll_to_load_all_speeches(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        try:
            # Check for multiple speech boxes appearing at once
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".speechesBox"))
            )
        except TimeoutException:
            # Break the loop if no new elements appear after 10 seconds
            break

        # Short sleep to allow content to load, adjust as needed
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# %%
# def fetch_speech_text(url):
#     options = webdriver.ChromeOptions()
#     options.headless = True

#     with closing(webdriver.Chrome(options=options)) as driver:
#         driver.get(url)
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "articleBody"))
#         )

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         title = soup.find("div", class_="TwitterLeft")
#         if title:
#             title = title.text.strip()
#         else:
#             title = None

#         content_elements = soup.find_all("p", style="text-align: justify;")
#         content = "\n".join([element.text.strip() for element in content_elements if "Speech Text" not in element.text])

#         date_element = soup.find_all("div", class_="TwitterLeft")
#         if date_element:
#             date_str = date_element[-1].text.strip().split(":")[1].strip()
#             try:
#                 date = dateutil.parser.parse(date_str, fuzzy=True).strftime("%Y-%m-%d")
#             except ValueError:
#                 date = None
#         else:
#             date = None

#     return title, content, date

def fetch_speech_text(driver, url):
    # Open the speech link in a new tab
    driver.execute_script(f"window.open('{url}', '_blank');")
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "articleBody"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find("div", class_="TwitterLeft")
    if title:
        title = title.text.strip()
    else:
        title = None

    content_elements = soup.find_all("p", style="text-align: justify;")
    content = "\n".join([element.text.strip() for element in content_elements if "Speech Text" not in element.text])

    # Close the current tab and switch back to the main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return title, content, soup.find("div", class_="pwdBy").text.strip()

# %%
def fetch_speech_links(start_date, end_date):
    options = webdriver.ChromeOptions()
    options.headless = True

    with closing(webdriver.Chrome(options=options)) as driver:
        url = "https://www.narendramodi.in/category/text-speeches"
        driver.get(url)

        # Input start and end dates
        start_date_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "fromdate"))
        )
        end_date_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "todate"))
        )
        start_date_input.clear()
        start_date_input.send_keys(start_date)
        end_date_input.clear()
        end_date_input.send_keys(end_date)

        # Click the "GO" button
        go_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchspeeches"))
        )
        go_button.click()

        # Wait for the initial speech boxes to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".speechesBox"))
        )

        scroll_to_load_all_speeches(driver)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll to the bottom and continue scrolling past the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollBy(0, 200);")  # Scroll past the bottom

            # Wait for a few seconds to allow the page to load additional content
            time.sleep(5)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Scroll again to the bottom to ensure no new content is loaded
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                final_height = driver.execute_script("return document.body.scrollHeight")
                if final_height == new_height:
                    break
            last_height = new_height

        # Parse the page source after all speech boxes have loaded
        speech_links = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for speech_box in soup.find_all(class_="speechesBox"):
            link = speech_box.find("a", class_="left_class", href=True)
            date = speech_box.find("div", class_="pwdBy").text.strip()
            title = speech_box.find("div", class_="speechesItemLink").text.strip()
            if link:
                speech_links.append({
                    "title": title,
                    "date": date,
                    "link": link['href']
                })

        return speech_links

# %%
def save_speech_to_file(title, content, date):
    if title is None or content is None or date is None:
        return

    file_name = re.sub(r'[\W_]+', '-', title.lower()) + ".txt"
    file_path = os.path.join(SPEECHES_DIR, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n")
            file.write(f"Date: {date}\n\n")
            file.write(content)
        print(f"Saved '{title}' to {file_path}")
    except Exception as e:
        print(f"Error saving '{title}' to {file_path}: {e}")

# %%
def main():
    if not os.path.exists(SPEECHES_DIR):
        os.makedirs(SPEECHES_DIR)

    end_date = datetime.now().strftime("%m/%d/%y")
    start_date = "01/01/24"
    speech_links = fetch_speech_links(start_date, end_date)

    total_speeches = len(speech_links)
    with closing(webdriver.Chrome()) as driver:
        for i, speech in enumerate(speech_links, start=1):
            try:
                title, content, date = fetch_speech_text(driver, speech['link'])  # Pass 'link' from the dictionary
                save_speech_to_file(title, content, date)
                print(f"Progress: {i}/{total_speeches} speeches scraped.")
            except Exception as e:
                print(f"Error scraping speech at {speech['link']}: {e}")

if __name__ == "__main__":
    main()

# %% [markdown]
# pip install selenium
# 
# pip install requests beautifulsoup4
# 
# pip install python-dateutil
# 


