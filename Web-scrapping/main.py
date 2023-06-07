import bs4.element
import requests

from fake_headers import Headers
from bs4 import BeautifulSoup

headers = Headers(browser='chrome', os = 'win')


def scrap_pages(number_of_pages: int):
    # Здесь проходимся по нужному числу страниц (на каждой странице по 20 статей)
    for page in range(1, number_of_pages + 1):
#

        # Get-запрос к странице с текущим номером
        response = requests.get(f"https://habr.com/ru/all/page{page}", headers=headers.generate()).text
        recent_articles = BeautifulSoup(response, "lxml")

#
        # Проходимся по списку статей на текущей странице
        for article in recent_articles.find_all("article", class_="tm-articles-list__item"):
#
#             # Вытаскиваем id очередной статьи и делаем Get-запрос к её странице
            link_to_article = f"https://habr.com/ru/articles/{article['id']}/"
            response = requests.get(link_to_article).text
            article_home_page = BeautifulSoup(response, "lxml")


            # Передаём полученную страницу статьи и ссылку на неё
            check_themes(article_home_page, link_to_article)


def check_themes(article: bs4.element.Tag, link_to_article: str) -> None:

    # Вытаскиваем элемент с темами (хэштегами) статьи и проверяем их на совпадение с нужными
    for theme in article.find_all("span", class_="tm-article-snippet__hubs-item"):

        # Если находим хотя бы одно совпадение, то печатаем информацию о статье
        if theme.text.strip() in ['Дизайн', 'Фото', 'Web', 'Python']:
            print_article_content(article, link_to_article)
            break


def print_article_content(article: bs4.element.Tag, link_to_article: str):
    date = article.find("time")["title"]
    title = article.find("h1", class_="tm-title tm-title_h1").text.strip()
    print(f"Article title: '{title}'\nDate of release: {date}\nLink: {link_to_article}")


if __name__ == "__main__":
    scrap_pages(10)
