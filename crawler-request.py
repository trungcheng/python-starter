from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import csv
import time

shop_page_url = "https://printerval.com/shop?page_id={}"
product_detail_url = "https://printerval.com{}"

product_url_file = "./assets/product_urls.txt"
product_file = "./assets/products.json"

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}

MAX_THREADS = 10
product_detail_list = []


def get_title(soup):
    try:
        title = soup.find(
            "h1", attrs={'class': 'product-heading js-product-name'})
        title_value = title.string
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""

    return title_string


def get_description(soup):
    try:
        desc = soup.find("div", attrs={"class": 'product-detail-description'})
        desc_content = desc.decode_contents()
    except AttributeError:
        desc_content = ""

    return desc_content


def get_price(soup):
    try:
        price = soup.find(
            "div", attrs={'class': 'product-detail-row product-price'}).string.strip()
    except AttributeError:
        price = ""

    return price


def get_old_price(soup):
    try:
        old_price = soup.find(
            "div", attrs={'class': 'product-detail-row product-high-price'}).string.strip()
    except AttributeError:
        old_price = ""

    return old_price


def get_color(soup):
    try:
        color = soup.find(
            "span", attrs={'id': 'color'}).string.strip()
    except AttributeError:
        color = ""

    return color


def get_type(soup):
    try:
        product_type = soup.find(
            "span", attrs={'id': 'type'}).string.strip()
    except AttributeError:
        product_type = ""

    return product_type


def get_style(soup):
    try:
        style = soup.find(
            "span", attrs={'id': 'style'}).string.strip()
    except AttributeError:
        style = ""

    return style


def get_size(soup):
    try:
        size = soup.find(
            "span", attrs={'id': 'size'}).string.strip()
    except AttributeError:
        size = ""

    return size


def get_rating(soup):
    try:
        rating = soup.find(
            "i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:

        try:
            rating = soup.find(
                "span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


def crawl_product_urls():
    product_urls = []
    i = 0

    while (i <= 9):
        print("Start crawl product url page: ", i)
        webpage = requests.get(shop_page_url.format(i), headers=headers)

        if (webpage.status_code != 200):
            break

        soup = BeautifulSoup(webpage.content, 'lxml')

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class': 'product-link'})

        if (len(links) == 0):
            break

        for link in links:
            product_urls.append(link.get("href"))

        print("End crawl product url page: ", i)

        i += 1

    return product_urls


def save_product_urls(product_urls=[]):
    file = open(product_url_file, "w+")
    str = "\n".join(product_urls)
    file.seek(0)
    file.truncate()
    file.write(str)
    file.close()


def crawl_url(url=''):
    webpage = requests.get(
        product_detail_url.format(url), headers=headers)

    new_soup = BeautifulSoup(webpage.content, "lxml")

    product_detail_list.append({
        'title': get_title(new_soup),
        'description': get_description(new_soup),
        'price': get_price(new_soup),
        'old_price': get_old_price(new_soup)
    })

    # time.sleep(0.25)
    print('Crawled ' + str(url))


def crawl_products(product_urls=[]):
    print("Crawl product starting...")

    threads = min(MAX_THREADS, len(product_urls))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(crawl_url, product_urls)

    file = open(product_file, "w+")
    file.seek(0)
    file.truncate()
    json.dump(product_detail_list, file, indent=4)
    file.close()

    print("Save file: ", product_file)


def main():
    product_urls = crawl_product_urls()

    print("Number of product urls: ", len(product_urls))

    save_product_urls(product_urls)

    t0 = time.time()

    crawl_products(product_urls)

    t1 = time.time()

    print(f"{t1-t0} seconds to download {len(product_urls)} products.")


main()
