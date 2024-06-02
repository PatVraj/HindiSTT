from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

driver = webdriver.Chrome()  

# Define the parameters for the request
language = 'hi'
page = 1
keyword = ''
fromdate = '04/13/2024'
todate = datetime.now().strftime("%m/%d/%Y")
filtertag = ''

speech_links = []

#while True:
    # Construct the URL for the AJAX request
    #url = f"https://www.narendramodi.in/speech/searchspeeche?language={language}&page={page}&keyword={keyword}&fromdate={fromdate}&todate={todate}&filtertag={filtertag}"
url = "https://www.narendramodi.in/hi/text-of-prime-minister-narendra-modis-speech-at-public-meeting-in-mirzapur-uttar-pradesh"
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
article = soup.find('article', class_='articleBody main_article_content')
# Extract the text content from all <p> tags within the article
text = '\n'.join([p.get_text() for p in article.find_all('p')])
print(text)


    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # for speech_box in soup.find_all(class_="speechesBox"):
    #     link = speech_box.find("a", class_="left_class", href=True)
    #     date = speech_box.find("div", class_="pwdBy").text.strip()
    #     if link:
    #         speech_links.append({
    #             "date": date,
    #             "link": link['href']
    #         })
    #break
print(speech_links)