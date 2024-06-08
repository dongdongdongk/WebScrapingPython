from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pandas as pd

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

# 드롭다운 메뉴 셀렉트 
dropdown = Select(driver.find_element(By.ID, 'country'))

dropdown.select_by_visible_text('Spain')

# 'tr' 요소가 나타날 때까지 최대 10초 대기
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))

# 모든 경기 데이터를 저장할 리스트 초기화
dates = []
home_teams = []
scores = []
away_teams = []

# 각 경기 데이터를 추출하여 리스트에 추가
matches = driver.find_elements(By.TAG_NAME, 'tr')
for match in matches:
    date = match.find_element(By.XPATH, './td[1]').text
    home_team = match.find_element(By.XPATH, './td[2]').text
    score = match.find_element(By.XPATH, './td[3]').text
    away_team = match.find_element(By.XPATH, './td[4]').text
    
    dates.append(date)
    home_teams.append(home_team)
    scores.append(score)
    away_teams.append(away_team)
    print(date)
    print(home_team)
    print(score)
    print(away_team)
    print(" ")


# 데이터 프레임 생성
df = pd.DataFrame({'date': dates, 'home_team': home_teams, 'score': scores, 'away_team': away_teams})

# CSV 파일로 저장
df.to_csv('Spain.csv', index=False)

# 데이터 프레임 출력 (옵션)
print(df)