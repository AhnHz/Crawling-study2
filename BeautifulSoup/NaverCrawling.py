import sys

import numpy as np
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = ("&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=26&mynews=0&office_type=0"
                       "&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=")

def get_link(keyword, page_range):
    link = []

    for page in range(page_range):
        # 1, 11, 21, 31, ...
        current_page = 1 + page * 10

        crawling_url = URL_BEFORE_KEYWORD + keyword + URL_BEFORE_PAGE_NUM + str(current_page)       # 문자로

        response = requests.get(crawling_url)
        # print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        url_tag = soup.select('a.news_tit')
        #print(url_tag)

        for url in url_tag:
            link.append(url['href'])

    #print(link)
    return link


def get_article(file1, link):
    with open(file1, 'w', encoding='utf8') as f:
        for url in link:
            article = Article(url, language='ko')

            try:
                article.download()
                article.parse()

            except:
                continue

            news_title = article.title
            news_content = article.text

            f.write(news_title)
            f.write(news_content)

    f.close()


def word_count(file1, file2):
    f = open(file1, 'r', encoding='utf8')
    g = open(file2, 'w', encoding='utf8')

    engine = Okt()
    data = f.read()
    all_nouns = engine.nouns(data)      # 명사 추출
    nouns = [i for i in all_nouns if (len(i)) > 1]
    #print(nouns)

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda x: x[1], reverse=True))
    #by_num = sorted(count.items(), key=lambda x: x[1], reverse=True)

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for i, j in zip(word, number):
        final = f'{i}       {j}'
        g.write(final + '\n')

    f.close()
    g.close()


    #print(by_num)
    return by_num, count


def top_n(count, file3):
    g = open(file3, 'w', encoding='utf-8')
    rank = count.most_common(10)

    word = [i for i in dict(rank).keys()]
    number = [i for i in dict(rank).values()]

    for i, j in zip(word, number):
        final = f'{i}       {j}'
        g.write(final + '\n')

    g.close()
    return rank


def full_vis_bar(by_num):
    for w, n in list(by_num.items()):
        if n <= 15:
            del by_num[w]       # 15개 이하면 삭제

    fig = plt.gcf()
    fig.set_size_inches(20, 10)     # 1 -> 100pixel, 20 -> 2000pixel
    matplotlib.rc('font', family='Apple SD Gothic Neo', size=10)
    plt.title('기사에 나온 전체 단어 개수', fontsize=30)
    plt.xlabel('기사에 나온 단어', fontsize=20)
    plt.ylabel('단어 개수', fontsize=20)
    plt.bar(by_num.keys(), by_num.values(), color='#6799FF')
    plt.xticks(rotation=45)
    plt.savefig('all_words.jpg')
    plt.show()


def topn_vis_bar(rank):
    topn_data = dict(rank)

    fig = plt.gcf()
    fig.set_size_inches(20, 10)  # 1 -> 100pixel, 20 -> 2000pixel
    matplotlib.rc('font', family='Apple SD Gothic Neo', size=10)
    plt.title('기사에 나온 10개 단어 개수', fontsize=30)
    plt.xlabel('기사에 나온 단어', fontsize=20)
    plt.ylabel('단어 개수', fontsize=20)
    plt.bar(topn_data.keys(), topn_data.values(), color='#ff9999')
    plt.xticks(rotation=45)
    plt.savefig('top10_words.jpg')
    plt.show()


def wordcloud(by_num):
    masking_image = np.array(Image.open('alice_mask.png'))
    wc = WordCloud(font_path='/System/Library/Fonts/AppleSDGothicNeo.ttc',
                   #background_color=(168, 237, 244),
                   background_color='white',
                   width=2500, height=1500,
                   mask=masking_image)
    cloud = wc.generate_from_frequencies(by_num)    # 딕셔너리가 필요
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud.jpg')
    plt.show()

def main(argv):
    print(argv)
    link = get_link(argv[1], int(argv[2]))      #  python NaverCrawling.py 르세라핌 2

    get_article('수집내용.txt', link)
    by_num, count = word_count('수집내용.txt', '워드카운트.txt')
    full_vis_bar(by_num)
    rank = top_n(count, '상위 10개.txt')
    topn_vis_bar(rank)
    wordcloud(by_num)

if __name__ == '__main__':
    main(sys.argv)
