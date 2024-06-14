from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# 사용자 에이전트(User-Agent)를 설정합니다
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

options = Options()

# options.add_experimental_option("detach", True)

# 사용자 에이전트를 설정합니다
options.add_argument(f"user-agent={user_agent}")

options.add_argument("window-size=1920x1080")


options.add_argument("--disable-blink-features=AutomationControlled")

# 서드 파티 쿠키 단계적 폐지 옵션 추가
options.add_argument("--test-third-party-cookie-phaseout")


website = 'https://www.audible.com/search'

driver = webdriver.Chrome(options=options)

driver.get(website)


# 페이지 네이션
pagination = driver.find_element(By.XPATH,'//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME,'li')
lastPage = int(pages[-2].text)


currentPage = 1
book_title = []
book_author = []
book_length = []


while currentPage <= lastPage:

    # 'tr' 요소가 나타날 때까지 최대 10초 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.adbl-impression-container ')))


    container = driver.find_element(By.CSS_SELECTOR,'.adbl-impression-container ')

    products = container.find_elements(By.CSS_SELECTOR,'.bc-list-item.productListItem')


    for product in products:
        book_title.append(product.find_element(By.XPATH,'.//h3[contains(@class,"bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH,'.//li[contains(@class,"authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH,'.//li[contains(@class,"runtimeLabel")]').text)
    
    currentPage = currentPage + 1

    try:
        nextPage = driver.find_element(By.XPATH,'//span[contains(@class,"nextButton")]')
        nextPage.click()
    except:
        pass 



df_book = pd.DataFrame({'제목' : book_title, '글쓴이' : book_author, '시간' : book_length })
df_book.to_csv('booksHeadless.csv', index=False)