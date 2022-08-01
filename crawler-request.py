from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import time
import random
import mysql.connector
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

DOMAIN = "https://printerval.com"

PRODUCT_DETAIL_URL = DOMAIN + "{}"

PRODUCT_URL_FILE = "./assets/product_urls.txt"

PRODUCT_FILE = "./assets/products.json"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}

MAX_THREADS = 10

product_detail_list = []


def get_title(soup):
    try:
        title = soup.find(
            'h1', attrs={'class': 'product-heading js-product-name'})
        title_value = title.string
        title_string = title_value.strip().replace('\n', '')
    except AttributeError:
        title_string = ''

    return title_string


def get_description(soup):
    try:
        desc = soup.find('div', attrs={'class': 'product-detail-description'})
        desc_content = desc.decode_contents().strip().replace('\n', '').replace('\\', '')
    except AttributeError:
        desc_content = ''

    return desc_content


def get_price(soup):
    try:
        price = soup.find(
            'div', attrs={'class': 'product-detail-row product-price'}).string.strip().replace('$', '')

        if price == '':
            price = None
    except AttributeError:
        price = None

    return price


def get_old_price(soup):
    try:
        old_price = soup.find(
            'div', attrs={'class': 'product-detail-row product-high-price'}).string.strip().replace('$', '')

        if old_price == '':
            old_price = None
    except AttributeError:
        old_price = None

    return old_price


def get_color(soup):
    try:
        colors = []
        colorElements = soup.find_all(
            'div', attrs={'class': 'js-choose-variant'})

        if (len(colorElements) > 0):
            for ele in colorElements:
                colors.append({
                    'title': ele.get('title').strip().replace('\n', ''),
                    'link': ele.find('img').get('src')
                })
    except AttributeError:
        colors = []

    return colors


def get_type(soup):
    try:
        types = []
        productTypes = soup.find_all(
            'label', attrs={'class': 'js-choose-variant'})

        if (len(productTypes) > 0):
            for pType in productTypes:
                types.append(pType.get('title').strip().replace('\n', ''))
    except AttributeError:
        types = []

    return types


def get_style(soup):
    try:
        styles = []
        productStyles = soup.find_all(
            'select', attrs={'name': 'variant-style'})

        if (len(productStyles) > 0):
            for pStyle in productStyles:
                options = pStyle.find_all('option')

                if (len(options) > 0):
                    for option in options:
                        styles.append({
                            'id': option.get('value').strip().replace('\n', ''),
                            'name': option.string.strip().replace('\n', '')
                        })
    except AttributeError:
        styles = []

    return styles


def get_size(soup):
    try:
        sizes = []
        productSizes = soup.find_all(
            'select', attrs={'name': 'variant-size'})

        if (len(productSizes) > 0):
            for pSize in productSizes:
                options = pSize.find_all('option')

                if (len(options) > 0):
                    for option in options:
                        sizes.append({
                            'id': option.get('value').strip().replace('\n', ''),
                            'name': option.string.strip().replace('\n', '')
                        })
        else:
            productSizes = soup.find_all(
                'li', attrs={'class': 'select-a-size'})

            if (len(productSizes) > 0):
                for pSize in productSizes:
                    sizes.append({
                        'id': pSize.get('data-variant-option-id').strip().replace('\n', ''),
                        'name': pSize.find('span').string.strip().replace('\n', '')
                    })
    except AttributeError:
        sizes = []

    return sizes


def get_print_location(soup):
    try:
        locations = []
        print_location = soup.find(
            'div', attrs={'class': 'print-location'})

        if print_location:
            locations = ['Front', 'Back']
    except AttributeError:
        locations = []

    return locations


def get_main_img(soup):
    try:
        main_img = ''
        main_img_wrapper = soup.find_all(
            'div', attrs={'class': 'product-gallery-item swiper-slide'})

        if (len(main_img_wrapper) > 0):
            main_img = main_img_wrapper[0].find(
                'source', attrs={'media': '(min-width: 1030px)'}).get('srcset')
    except AttributeError:
        main_img = ''

    return main_img


def get_sub_img_1(soup):
    try:
        sub_img_1 = ''
        sub_img_1_wrapper = soup.find_all(
            'div', attrs={'class': 'product-gallery-item swiper-slide'})

        if (len(sub_img_1_wrapper) > 0):
            sub_img_1 = sub_img_1_wrapper[1].find(
                'source', attrs={'media': '(min-width: 1030px)'}).get('srcset')
    except AttributeError:
        sub_img_1 = ''

    return sub_img_1


def get_sub_img_2(soup):
    try:
        sub_img_2 = ''
        sub_img_2_wrapper = soup.find_all(
            'div', attrs={'class': 'product-gallery-item swiper-slide'})

        if (len(sub_img_2_wrapper) > 0):
            sub_img_2 = sub_img_2_wrapper[2].find(
                'source', attrs={'media': '(min-width: 1030px)'}).get('srcset')
    except AttributeError:
        sub_img_2 = ''

    return sub_img_2


def unique(list):
    x = np.array(list)

    return np.unique(x)


def crawl_product_cates(cate_arr):
    product_url_arr = []

    if (len(cate_arr) > 0):
        i = 1
        for cate in cate_arr:
            product_urls = crawl_product_urls(cate, i)
            save_product_urls(product_urls)
            crawl_products(product_urls, i)
            product_url_arr += product_urls
            i += 1

    return len(product_url_arr)


def crawl_product_urls(url, cate_id):
    product_urls = []
    i = 0

    while (i != -1):
        print('Start crawl product url page ' +
              str(i) + ' of category id ' + str(cate_id))

        webpage = requests.get(url.format(i), headers=HEADERS)

        if (webpage.status_code != 200):
            break

        soup = BeautifulSoup(webpage.content, 'lxml')

        links = soup.find_all('a', attrs={'class': 'product-link'})

        if (len(links) == 0):
            i = -1
            break

        for link in links:
            product_urls.append({
                'link': link.get('href'),
                'cat_id': cate_id
            })

        print('End crawl product url page ' + str(i) +
              ' of category id ' + str(cate_id))

        i += 1

    return product_urls


def save_product_urls(product_urls=[]):
    file = open(PRODUCT_URL_FILE, 'a', encoding='utf-8')
    # str = "\n".join(product_urls)
    # file.write(str)
    json.dump(product_urls, file, indent=4)
    file.close()


def crawl_url(link, cat_id):
    webpage = requests.get(
        PRODUCT_DETAIL_URL.format(link), headers=HEADERS)

    new_soup = BeautifulSoup(webpage.content, 'lxml')

    product_detail_list.append({
        'cat_id': cat_id,
        'author_id': random.randint(1, 10),
        'title': get_title(new_soup),
        'description': get_description(new_soup),
        'price': get_price(new_soup),
        'old_price': get_old_price(new_soup),
        'colors': get_color(new_soup),
        'types': get_type(new_soup),
        'styles': get_style(new_soup),
        'sizes': get_size(new_soup),
        'print_locations': get_print_location(new_soup),
        'main_img': get_main_img(new_soup),
        'sub_img_1': get_sub_img_1(new_soup),
        'sub_img_2': get_sub_img_2(new_soup),
    })

    # time.sleep(0.25)
    print('Crawled ' + str(link))


def crawl_products(product_urls, cate_id):
    print('Crawl product of category id ' + str(cate_id) + ' starting...')

    threads = min(MAX_THREADS, len(product_urls))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda f: crawl_url(**f), product_urls)

    file = open(PRODUCT_FILE, 'a', encoding='utf-8')
    json.dump(product_detail_list, file, indent=4)
    file.close()

    print('Save file: ', PRODUCT_FILE)


def insert_to_mysql():
    try:
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_DATABASE')
        user = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')

        connection = mysql.connector.connect(
            host=host, database=database, user=user, password=password, port=port)

        cursor = connection.cursor()

        sql = "INSERT INTO `products` (`cat_id`, `author_id`, `title`, `description`, `price`, `old_price`, `colors`, `types`, `styles`, `sizes`, `print_locations`, `main_img`, `sub_img_1`, `sub_img_2`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        with open(PRODUCT_FILE, 'r') as file:
            data = json.load(file)

        insert_array = convert_data(data)

        cursor.executemany(sql, insert_array)

        connection.commit()

        print(cursor.rowcount, "Record inserted successfully!")
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table! {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def convert_data(data):
    insert_array = []

    if (len(data) > 0):
        for item in data:
            convert_keys = ['colors', 'types',
                            'styles', 'sizes', 'print_locations']
            for key in convert_keys:
                if isinstance(item[key], list):
                    item[key] = str(item[key])

            values = tuple(item.values())
            insert_array.append(values)

    return insert_array


def clean_file():
    file1 = open(PRODUCT_URL_FILE, 'w+')
    file2 = open(PRODUCT_FILE, 'w+')

    file1.truncate()
    file2.truncate()


def get_categories():
    categories = []

    webpage = requests.get(DOMAIN, headers=HEADERS)

    if (webpage.status_code != 200):
        return []

    soup = BeautifulSoup(webpage.content, 'lxml')

    level1_links = soup.find_all('a', attrs={'class': 'navigation-link'})

    if (len(level1_links) > 0):
        for link in level1_links:
            if link.get('href') != '#' and DOMAIN in link.get('href') and link.get('href') != 'https://printerval.com/create-your-own':
                categories.append(link.get('href') + '?page_id={}')

    level2_links = soup.find_all('a', attrs={'class': 'lev2-link'})

    if (len(level2_links) > 0):
        for link in level2_links:
            if link.get('href') != '#':
                if DOMAIN not in link.get('href'):
                    categories.append(PRODUCT_DETAIL_URL.format(
                        link.get('href')) + '?page_id={}')
                else:
                    categories.append(link.get('href')[1:] + '?page_id={}')

    level3_links = soup.find_all('a', attrs={'class': 'lev3-link'})

    if (len(level3_links) > 0):
        for link in level3_links:
            if link.get('href') != '#':
                if DOMAIN not in link.get('href'):
                    if '?' in link.get('href'):
                        categories.append(
                            PRODUCT_DETAIL_URL.format(link.get('href')) + '&page_id={}')
                    else:
                        categories.append(
                            PRODUCT_DETAIL_URL.format(link.get('href')) + '?page_id={}')
                else:
                    if '?' in link.get('href'):
                        categories.append(link.get('href') + '&page_id={}')
                    else:
                        categories.append(link.get('href') + '?page_id={}')

    return unique(categories)


def main_crawl(categories):
    t0 = time.time()

    len_products = crawl_product_cates(categories)

    t1 = time.time()

    print(f'{t1-t0} seconds to download {len_products} products.')


def main():
    clean_file()

    categories = get_categories()

    main_crawl(categories)

    insert_to_mysql()


if __name__ == '__main__':
    main()
