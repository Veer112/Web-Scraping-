import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin


def sanitize_filename(filename):
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename


def download_webpage(url, output_folder):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            if href.startswith('http'):
                download_webpage(href, output_folder)
            else:
                download_url = urljoin(url, href)
                parsed_url = urlparse(download_url)
                download_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path

                filename = href.rsplit('/', 1)[-1]
                filename = sanitize_filename(filename)
                output_path = os.path.join(output_folder, filename)

                if os.path.exists(output_path):
                    print(f"Skipped: {download_url}")
                    continue

                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(output_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded: {download_url}")
                else:
                    print(f"Failed to download: {download_url}")


webpage_url = 'https://docs.webmethods.io/#gsc.tab=0'
output_folder = 'C:/Users/HP/Desktop/assgn/gptscrpe/downloaded_pages'


os.makedirs(output_folder, exist_ok=True)

download_webpage(webpage_url, output_folder)
