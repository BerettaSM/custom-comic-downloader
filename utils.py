import os
import time

import requests
import bs4

BASE_URL = 'https://www.exocomics.com/'


def find_last_comic_num() -> int:

    response = requests.get(url=BASE_URL)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        raise ValueError("Couldn't retrieve last comic number.")

    soup = bs4.BeautifulSoup(markup=response.text, features='html.parser')
    num_elem = soup.select_one('div.numbers')
    num = int(''.join(num_elem.get_text().split()))

    return num


def download(range_start: int, range_end: int, dest: str, stats: dict) -> None:

    for n in range(range_start, range_end):

        target_comic_url = BASE_URL + f'{n:02d}/'

        response = requests.get(url=target_comic_url)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            print(f'Error during request to number {n}. Skipping...')
            continue

        soup = bs4.BeautifulSoup(markup=response.text, features='html.parser')
        img_elem = soup.select_one('img.image-style-main-comic')

        if not img_elem:
            print(f'Comic {n} is not an image. Skipping...')
            continue

        img_url = BASE_URL + img_elem.get('src')
        img_response = requests.get(url=img_url)
        try:
            img_response.raise_for_status()
        except requests.HTTPError:
            print(f'Error during image download. Image url: {img_url}.\nSkipping...')
            continue

        filename = os.path.split(img_url)[-1]
        with open(os.path.join(dest, filename), 'wb') as file:
            for chunk in img_response.iter_content(100000):
                file.write(chunk)

        print(f'Comic from ({target_comic_url}) downloaded.')
        stats['downloads'] += 1

        time.sleep(1)  # At site's request in robot.txt
