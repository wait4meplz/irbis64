import sys

import img2pdf
import requests
from bs4 import BeautifulSoup
from os import path


def get_html(url: str, headers: dict = None) -> str:
    page = requests.get(url=url, headers=headers)
    return page.text


def get_content(url: str, headers: dict = None) -> bytes:
    page = requests.get(url=url, headers=headers)
    return page.content


def get_soup(soup: str) -> BeautifulSoup:
    soup = BeautifulSoup(soup, 'lxml')
    return soup


def get_card_data(soup_page) -> list:
    cards = soup_page.find_all(attrs={'style': 'width:100%;border:1px;font-size:11px;'})
    result = []
    for card in cards:
        link_blocks = card.next_sibling.next_sibling
        if link_blocks.name == 'div':
            link = link_blocks['id'].split('_')[-1]
            data_card = card.text.split('. - ')
            count_pages = int(data_card[2][:-2])
            filename = data_card[0].split('  \xa0\xa0\xa0 ')[2].split(':')[0][:100]
            image_path = card.find('img', attrs={'style': 'float:left; margin:10px; width:120px;'})['src'] \
                .split('&')[3].split('=')[1].replace('%5C', '\\').replace('%2E', '.')
            image_id = 'GUEST'
            result.append((link, count_pages, image_path, image_id, filename))
    return result


def write_pdf(data: list[bytes], path_to_file: str) -> None:
    with open(path_to_file, 'wb') as file:
        file.write(img2pdf.convert(data))


def get_books(data: tuple) -> None:
    (image_file_mfn, file_page, image, image_id, filename) = data
    pages = []
    for current_page in range(1, file_page + 1):
        image_page = f'http://webirbis.tsogu.ru/cgi-bin/irbis64r_plus/cgiirbis_64_ft.exe?C21COM=7&I21DBN=VSR_READER&P21DBN=VSR&IMAGE_FILE_NAME={image}&IMAGE_FILE_MFN={image_file_mfn}&Z21ID={image_id}&FILE_PAGE={current_page}&S21AllTRM=&'
        data = get_content(image_page)
        pages.append(data)
        print(f'[INFO] {current_page}/{file_page} - {filename}')
    path_to_file = f'{path.abspath("./")}/data/{filename}.pdf'
    write_pdf(pages, path_to_file)


def main2(url: str) -> None:
    html_page = get_html(url)
    soup_page = get_soup(html_page)
    result = get_card_data(soup_page)
    for book in result:
        get_books(book)


#if __name__ == '__main__':
    #url = 'http://webirbis.tsogu.ru/cgi-bin/irbis64r_plus/cgiirbis_64_ft.exe?S21COLORTERMS=0&LNG=&Z21ID=GUEST&I21DBN=VSR_FULLTEXT&P21DBN=VSR&S21STN=1&S21REF=10&S21FMT=briefHTML_ft&S21CNR=5&C21COM=S&S21ALL=%3C.%3EI=%2D806577353%3C.%3E&USES21ALL=1'
#main(url)
