import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from newspaper import Article, Config
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
to_df = []
total_by_num = {}

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

# 기사 크롤링
for link in link_list:

    article = Article(link, config=config)

    try:
        article.download()
        article.parse()
    except:
        continue

    news_title = article.title
    news_content = article.text.strip().replace('\n', '')

    engine = Okt()
    all_nouns = engine.nouns(news_content)      # 명사 추출
    nouns = [i for i in all_nouns if (len(i)) > 1]      # 한글자 이상 단어만
    count = Counter(nouns)

    del count[keyword]      # 검색어 제거
    del count[keyword[-2:]]
    by_num = sorted(count.items(), key=lambda x: x[1], reverse=True)
    top5 = ','.join([keyword for keyword, count in by_num[:5]])     # 정렬 후 상위 5개만

    total_by_num.update(by_num)     # 기사별 상위 5개 단어들만 모으기

    data = [news_title, news_content, link, top5]
    to_df.append(data)

# 데이터프레임 생성 후 -> csv 파일로 저장
df = pd.DataFrame(to_df, columns=['제목', '내용', 'URL', '상위 단어 5개'])
df.to_csv('Selenium_naver_news_' + keyword + '.csv', encoding='utf-8')

# WordCloud 그리기
wc = WordCloud(font_path='/System/Library/Fonts/AppleSDGothicNeo.ttc',
                background_color='white',
                colormap='ocean',
                width=1200, height=800)

matplotlib.rc('font', family='Apple SD Gothic Neo', size=10)
cloud = wc.generate_from_frequencies(total_by_num)    # 딕셔너리가 필요
plt.imshow(cloud, interpolation='bilinear')
plt.title(keyword + ' 관련 기사별 상위 5개 단어들', pad=20, color='gray')
plt.axis('off')
plt.savefig('naver_news_' + keyword + '.jpg', dpi=300)
plt.show()


'''
    if article.text:
        print("제목:", article.title)
        print("내용:", article.text)
    else:
        print("제목:", article.title)
        print("내용:", "기사 내용을 가져올 수 없습니다.")


    print("링크:", link)
    print("=" * 50)
'''

driver.close()