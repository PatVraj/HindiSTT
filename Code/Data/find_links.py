from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

# Define the parameters for the request
language = 'hi'
page = 1
keyword = ''
fromdate = '03/17/2024'
todate =  '06/04/2024' #datetime.now().strftime("%m/%d/%Y")
filtertag = ''

speech_links = []

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

# Write the speech links and dates to a text file
with open("speech_links.txt", "w", encoding="utf-8") as file:
    for speech in speech_links:
        file.write(f"Date: {speech['date']}\nLink: {speech['link']}\n\n")

print("Speech links and dates have been saved to speech_links.txt")

# Close the WebDriver
driver.quit()
