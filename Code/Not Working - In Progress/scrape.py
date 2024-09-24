import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
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
    return text

def append_to_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content + '\n\n')

# URL to scrape
url = input("Enter the URL to scrape: ")

# Scrape the text from the URL
scraped_text = scrape_text_from_url(url)

# Filename to store the scraped text
output_filename = 'ECOC.txt'

# Append the scraped text to the file
append_to_file(output_filename, scraped_text)

print("Scraped text appended to", output_filename)
