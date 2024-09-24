from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# Initialize WebDriver


# Define the parameters for the request
language = 'hi'
page = 1
keyword = ''
fromdate = '03/17/2024'
todate =  '06/04/2024' # Or datetime.now().strftime("%m/%d/%Y")
filtertag = ''

speech_links = []

# Loop to get all the speech links and dates
while True:
    # Construct the URL for the AJAX request
    url = f"https://www.narendramodi.in/speech/searchspeeche?language={language}&page={page}&keyword={keyword}&fromdate={fromdate}&todate={todate}&filtertag={filtertag}"
    driver.get(url)
    
    # Wait for the page to load completely
    driver.implicitly_wait(20)
    
    # Get the page source
    page_source = driver.page_source
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find all speech boxes
    speech_boxes = soup.find_all(class_="speechesBox")
    
    # Check if there are no speech boxes on the page
    if not speech_boxes:
        break
    
    # Collect speech links and dates
    for speech_box in speech_boxes:
        link = speech_box.find("a", class_="left_class", href=True)
        date = speech_box.find("div", class_="pwdBy").text.strip()
        if link:
            speech_links.append({
                "date": date,
                "link": link['href']
            })
    
    # Increment the page number
    page += 1

# Directory to save HTML files
output_dir = 'speech_html_files'
os.makedirs(output_dir, exist_ok=True)

for i, speech in enumerate(speech_links):
    try:
        driver.get(speech['link'])
        driver.implicitly_wait(20)
        
        # Get the entire HTML of the page
        html_content = driver.page_source
        
        # Create a filename based on the speech index and date
        filename = os.path.join(output_dir, f"speech_{i+1}_{speech['date'].replace(' ', '_').replace(',', '')}.html")
        
        # Save the HTML content to a file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
            
        print(f"Saved {filename}")
    
    except TimeoutException:
        print(f"Timeout occurred while trying to load {speech['link']}. Skipping...")

# Close the WebDriver
driver.quit()