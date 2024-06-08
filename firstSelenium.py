from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()

options.add_experimental_option("detach", True)

website = 'https://www.adamchoi.co.uk/overs/detailed'

driver = webdriver.Chrome(options=options)

driver.get(website)

all_matches_button = driver.find_element(By.XPATH,'//label[@analytics-event="All matches"]')

all_matches_button.click()

# 'tr' 요소가 나타날 때까지 최대 10초 대기
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))


# //tr/td[1] 이걸 찾아야함 
matches = driver.find_elements(By.TAG_NAME,'tr')

for match in matches:
    date = match.find_element(By.XPATH,'./td[1]') # //tr/td[1]
    home_team = match.find_element(By.XPATH,'./td[2]') 
    score = match.find_element(By.XPATH,'./td[3]') 
    away_team = match.find_element(By.XPATH,'./td[4]') 

    print("날짜", date.text)
    print("홈팀", home_team.text)
    print("점수", score.text)
    print("상대팀", away_team.text)
    print(" ")
    print(" ")