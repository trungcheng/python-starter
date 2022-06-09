import requests
import shutil
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool


def download_image(url):
    res = requests.get(url, stream=True)

    if res.status_code == 200:
        with open("assets/img.png", "wb") as out_file:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, out_file)

        print("Download image successfully!")


def download_url_parallel(url):
    print("Downloading: ", url)
    # assumes that the last segment after the / represents the file name
    # if url is abc/xyz/file.txt, the file name will be file.txt
    file_name_start_pos = url.rfind("/") + 1
    file_name = url[file_name_start_pos:]

    res = requests.get(url, stream=True)
    if res.status_code == requests.codes.ok:
        with open("assets/" + file_name, "wb") as out_file:
            for data in res:
                out_file.write(data)

    return url


urls = [
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/comments",
    "https://jsonplaceholder.typicode.com/photos",
    "https://jsonplaceholder.typicode.com/todos",
    "https://jsonplaceholder.typicode.com/albums"
]

# Download an single image
download_image("http://craphound.com/images/1006884_2adf8fc7.jpg")

# Run multiple threads base on CPU count. Each call will take the next element in urls list
cpus = cpu_count()
results = ThreadPool(cpus - 1).imap_unordered(download_url_parallel, urls)
for result in results:
    print(result)
