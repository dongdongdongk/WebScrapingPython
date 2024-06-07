from bs4 import BeautifulSoup
import requests
import time
import re

# 사용하지 못하는 문자를 파일명에서 제거하는 함수
def clean_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

root = 'https://subslikescript.com'
website = f'{root}/movies'
result = requests.get(website)
content = result.text



soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

#페이지 네이션
pagination = soup.select_one('.pagination')
pages = pagination.select('.page-item')
last_page = pages[-2].text

for page in range(1, int(last_page) + 1): # range(1, 92+1)
    # https://subslikescript.com/movies?page=2
    result = requests.get(f'{website}?page={page}')
    print(f'현재페이지{website}?page={page}')
    content = result.text 
    soup = BeautifulSoup(content, 'lxml')
    box = soup.select_one('.main-article')


    # 'article.main-article' 내의 모든 'a' 태그를 선택
    a_tags = box.select('a')

    # 각 'a' 태그의 'href' 속성을 추출하여 'links' 배열에 저장
    links = [a.get('href') for a in a_tags]

    # 2개의 링크만 추출
    limited_links = links[:2]

    print(links)


    for link in limited_links:
        try:
            print(link)
            time.sleep(1)
            result = requests.get(f'{root}/{link}')
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.select_one('article.main-article')
            title = box.select_one('h1').get_text()
            transcript = box.select_one('.full-script').get_text(strip=True, separator=' ')

            # 파일명을 깨끗하게 정리
            clean_title = clean_filename(title)
            with open(f'{clean_title}.txt', 'w', encoding='utf-8') as file:
                file.write(transcript)
        except:
            print('=======링크 스크래핑에 실패하였습니다.======')
            print(link)
            pass
