from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get('https://www.narendramodi.in/category/text-speeches')

# Define the parameters for the request
language = 'hi'
page = 1
keyword = ''
fromdate = '04/13/2024'
todate = datetime.now().strftime("%m/%d/%Y")
filtertag = ''

# Construct the URL for the AJAX request
url = f"https://www.narendramodi.in/speech/searchspeeche?language={language}&page={page}&keyword={keyword}&fromdate={fromdate}&todate={todate}&filtertag={filtertag}"

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

# Extract the speech items and dates
speech_data = []
for box in speech_boxes:
    speech_item = box.select_one('.speechesItem')
    date_element = box.select_one('.pwdBy')
    if speech_item and date_element:
        speech_text = speech_item.get_text(strip=True)
        date_text = date_element.get_text(strip=True)
        speech_data.append((speech_text, date_text))

# Print the speech data
for speech, date in speech_data:
    print(f"Date: {date}")
    print(f"Speech: {speech}")
    print("-" * 20)

# Close the browser
driver.quit()