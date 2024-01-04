import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import pandas as pd

url = "https://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


library = []

results = soup.find_all('h3')
for title in results:
    book_url = url + title.find('a')['href']
    book_page = requests.get(book_url)
    book_soup = BeautifulSoup(book_page.content, 'html.parser')

    book_results = book_soup.find('h1').text
    price_results = book_soup.find('p', class_='price_color').text
    book_category = book_soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
    book_availability = book_soup.find('p', class_='availability').text.strip()
    library.append([book_results, price_results, book_category, book_availability])

for pages in range(2, 51):
    url = f'https://books.toscrape.com/catalogue/page-{pages}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('h3')
    for title in results:
        book_url = "https://books.toscrape.com/catalogue/" + title.find('a')['href']
        book_page = requests.get(book_url)
        book_soup = BeautifulSoup(book_page.content, 'html.parser')

        book_results = book_soup.find('h1').text
        price_results = book_soup.find('p', class_='price_color').text
        book_category = book_soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
        book_availability = book_soup.find('p', class_='availability').text.strip()

        library.append([book_results, price_results, book_category, book_availability])


df = pd.DataFrame(library, columns=['books', 'prices', 'categories', 'availability'])

df.to_csv('books_scraped.csv', index=False)



