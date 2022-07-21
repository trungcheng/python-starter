from bs4 import BeautifulSoup
import requests
import json
import csv

shop_page_url = "https://printerval.com/shop"
product_detail_url = "https://printerval.com{link}"

product_url_file = "./assets/product_urls.txt"
product_file = "./assets/products.txt"

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}


def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""

    return title_string


def get_description(soup):
    try:
        desc = soup.find("span", attrs={"id": 'productDesc'})
        desc_value = desc.string
        desc_string = desc_value.strip()
    except AttributeError:
        desc_string = ""

    return desc_string


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find(
            "span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        price = ""

    return price


# Function to extract Product Rating
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


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


def crawl_product_urls():
    product_urls = []
    # i = 1
    # while (i == 1):
    # print("Crawl page: ", i)
    # response = requests.get(shop_page_url.format(i))
    webpage = requests.get(shop_page_url, headers=headers)

    # if (webpage.status_code != 200):
    #     break

    soup = BeautifulSoup(webpage.content, 'lxml')

    # link_product_ele = parser.findAll(class_="styles__link--3QJ5N")
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': 'product-link'})

    # if (len(products) == 0):
    #     break

    for link in links:
        product_urls.append(link.get("href"))

        # i += 1

    # return product_list, i
    return product_urls


def save_product_urls(product_urls=[]):
    file = open(product_url_file, "w+")
    str = "\n".join(product_urls)
    file.write(str)
    file.close()
    print("Save file: ", product_url_file)


def crawl_product(product_urls=[]):
    product_detail_list = []
    key = 0

    for product_url in product_urls:
        webpage = requests.get(
            product_detail_url.format(product_url), headers=headers)

        new_soup = BeautifulSoup(webpage.content, "lxml")

        product_detail_list[key]['title'] = get_title(new_soup)
        product_detail_list[key]['description'] = get_description(new_soup)
        product_detail_list[key]['price'] = get_price(new_soup)
        product_detail_list[key]['rating'] = get_price(new_soup)
        product_detail_list[key]['review_count'] = get_price(new_soup)

        key += 1

    return product_detail_list


# flatten_field = ["badges", "inventory", "categories", "rating_summary",
#                  "brand", "seller_specifications", "current_seller", "other_sellers",
#                  "configurable_options",  "configurable_products", "specifications", "product_links",
#                  "services_and_promotions", "promotions", "stock_item", "installment_info"]


# def adjust_product(product):
#     e = json.loads(product)
#     if not e.get("id", False):
#         return None

#     for field in flatten_field:
#         if field in e:
#             e[field] = json.dumps(
#                 e[field], ensure_ascii=False).replace('\n', '')

#     return e


# def save_raw_product(product_detail_list=[]):
#     file = open(product_data_file, "w+")
#     str = "\n".join(product_detail_list)
#     file.write(str)
#     file.close()
#     print("Save file: ", product_data_file)


# def load_raw_product():
#     file = open(product_data_file, "r")
#     return file.readlines()


# def save_product_list(product_json_list):
#     file = open(product_file, "w")
#     csv_writer = csv.writer(file)

#     count = 0
#     for p in product_json_list:
#         if p is not None:
#             if count == 0:
#                 header = p.keys()
#                 csv_writer.writerow(header)
#                 count += 1
#             csv_writer.writerow(p.values())
#     file.close()
#     print("Save file: ", product_file)


product_urls = crawl_product_urls()

# print("No. Page: ", page)
print("Number of product urls: ", len(product_urls))

# save product id for backup
save_product_urls(product_urls)

# # crawl detail for each product id
# product_list = crawl_product(product_list)

# # save product detail for backup
# save_raw_product(product_list)

# # product_list = load_raw_product()
# # flatten detail before converting to csv
# product_json_list = [adjust_product(p) for p in product_list]
# # save product to csv
# save_product_list(product_json_list)
