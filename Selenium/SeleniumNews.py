from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from newspaper import Article, Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keyword = input('수집할 키워드를 입력하세요 : ')
page_num = input('수집할 페이지 번호 입력하세요 : ')

# 네이버 메인페이지 로드
driver = webdriver.Chrome()
driver.get('https://www.naver.com')

# 검색창 클릭
driver.find_element(By.CLASS_NAME, 'search_input_box').click()
time.sleep(2)

# 검색 키워드 입력 후 -> 검색 버튼 클릭
driver.find_element(By.CLASS_NAME, 'search_input').send_keys(keyword)
driver.find_element(By.CLASS_NAME, 'btn_search').submit()
time.sleep(2)

# 뉴스 탭 클릭
driver.find_element(By.LINK_TEXT, '뉴스').click()
time.sleep(2)

# 원하는 페이지로 이동
driver.find_element(By.LINK_TEXT, page_num).click()
time.sleep(2)

'''
list_news = driver.find_element(By.CLASS_NAME, 'list_news')
list_news_id = list_news.find_elements(By.TAG_NAME, 'li')
'''

# 뉴스별 url 가져오기
news_url = driver.find_elements(By.CLASS_NAME, 'news_tit')

link_list = []

for url in news_url:
    link = url.get_attribute('href')
    if link:
        link_list.append(link)

# 링크 출력
for link in link_list:
    print(link)

config = Config()
config.request_timeout = 10
config.ignore_ssl_verification = True

for link in link_list:

    article = Article(link, config=config)
    article.download()
    article.parse()

    if article.text:
        print("제목:", article.title)
        print("내용:", article.text)
    else:
        print("제목:", article.title)
        print("내용:", "기사 내용을 가져올 수 없습니다.")

    print("링크:", link)
    print("=" * 50)

driver.close()