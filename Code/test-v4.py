from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Set the script timeout to 60 seconds
driver.set_script_timeout(60)

# Navigate to the website
driver.get('https://www.narendramodi.in/category/text-speeches')

# Define the parameters for the request
language = 'hi'
page = 1
keyword = ''
fromdate = '04/13/2024'
todate = datetime.now().strftime("%m/%d/%Y")
filtertag = ''

speech_links = []

while True:
    # Construct the URL for the AJAX request
    url = f"https://www.narendramodi.in/speech/searchspeeche?language={language}&page={page}&keyword={keyword}&fromdate={fromdate}&todate={todate}&filtertag={filtertag}"
    
    try:
        # Execute JavaScript to make the AJAX request
        response_html = driver.execute_async_script("""
            var url = arguments[0];
            var callback = arguments[arguments.length - 1];

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    callback(xhr.responseText);
                }
            };
            xhr.send();
        """, url)

        # Parse the HTML response
        soup = BeautifulSoup(response_html, 'html.parser')

        # Find all the speech boxes
        speech_boxes = soup.select('.speechesBox')

        if not speech_boxes:
            break  # Exit the loop if no speeches are found

        # Extract the speech links and dates
        for box in speech_boxes:
            link_element = box.select_one('.speechesItemLink a')
            date_element = box.select_one('.pwdBy')
            if link_element and date_element:
                speech_link = link_element['href']
                date_text = date_element.get_text(strip=True)
                speech_links.append((speech_link, date_text))

        # Move to the next page
        page += 1
        time.sleep(1)  # Add a delay to avoid overwhelming the server

    except TimeoutException:
        print(f"Timeout occurred for page {page}. Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying

# Save the speech links and dates to a text file
with open('speech_links.txt', 'w') as file:
    for link, date in speech_links:
        file.write(f"Date: {date}\n")
        file.write(f"Link: {link}\n")
        file.write("-" * 20 + "\n")

# Close the browser
driver.quit()
