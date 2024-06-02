import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()  
url = "https://www.narendramodi.in/category/text-speeches"
driver.get(url)

class infinite_scroll(object):
    def __init__(self, last):
      self.last = last

    def __call__(self, driver):
        new = driver.execute_script('return document.body.scrollHeight')  
        if new > self.last:
            return new
        else:
            return False
    
last_height = driver.execute_script('return document.body.scrollHeight')
flag=1
while flag==1:
    # time.sleep(2)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(60)
    try:
        wait = WebDriverWait(driver, 6)
        new_height = wait.until(infinite_scroll( last_height))
        last_height = new_height

    except:
        print("End of page reached")
        flag = 0




