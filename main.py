"""tm-articles-list article <h2 class="tm-title tm-title_h2"> <a href="/ru/news/803825/" data-article-link="true"
class="tm-title__link"><span>PyPI временно приостановил регистрацию пользователей</span></a></h2> post-content-body
<time datetime="2024-03-29T07:08:01.000Z" title="2024-03-29, 09:08">9 часов назад</time> <div
class="article-formatted-body article-formatted-body article-formatted-body_version-2"><p>На сайте hackerrank.com
есть отличная <a href="https://www.hackerrank.com/challenges/xor-subsequence/problem" rel="noopener noreferrer
nofollow">задача</a>.<br>По заданному массиву <code>short[] A;</code> найти максимальное количество его подмассивов,
<code>xor</code> элементов которых будет одинаковым. Сам этот <code>xor</code> тоже нужно найти.</p><p>Максимальная
длина массива равна 10<sup>5</sup>, так что квадратичный алгоритм не укладывается в лимит по времени исполнения. Я в
своё время с этой задачей не справился и сдался, решив подсмотреть авторское решение. И в этот момент я понял почему
не справился - автор предлагал решать задачу через дискретное преобразование Фурье.</p><p></p></div>"""
import re

import bs4
import requests
from fake_headers import Headers


def get_headers():
    return Headers(os="win", browser="chrome").generate()


def search_key_words(preview_text):
    pattern = r"|".join(KEYWORDS)
    res_search = re.search(pattern, preview_text)
    return res_search


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

response = requests.get("https://habr.com/ru/articles/", headers=get_headers())
main_html_data = response.text

main_soup = bs4.BeautifulSoup(main_html_data, features="lxml")

tag_div_article_list = main_soup.find("div", class_="tm-articles-list")

article_tags = tag_div_article_list.find_all("article")

parsed_data = []

for article_tag in article_tags:
    h2_tag = article_tag.find("h2", class_="tm-title tm-title_h2")
    a_tag = h2_tag.find("a")
    relative_link = a_tag["href"]
    absolute_link = f"https://habr.com{relative_link}"
    time_tag = article_tag.find("time")
    pub_time = time_tag["datetime"]
    title = h2_tag.text
    preview_tag = article_tag.find("div", class_="article-formatted-body")
    preview = preview_tag.text

    # time.sleep(0.2)
    # article_response = requests.get(absolute_link, headers=get_headers())
    # article_html_data = article_response.text
    # article_soup = bs4.BeautifulSoup(article_html_data, features="lxml")
    #
    # full_article_tag = article_soup.find("div", id="post-content-body")
    # article_text = full_article_tag.text

    res = search_key_words(preview)
    if res is not None:
        parsed_data.append(
            {
                "title": title,
                "pub_time": pub_time,
                "link": absolute_link
                # "preview": preview[:20],
            }
        )

# print(parsed_data)
for article in parsed_data:
    print(f'{article["pub_time"]} - {article["title"]} - {article["link"]}')
