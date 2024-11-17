"""
title: decryption google doc url message
author: J. Hu
date: 17.11.2024
"""


import requests
from bs4 import BeautifulSoup
import re
import json


def request_url(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        url_text = response.content.decode('UTF-8')
        url_soup = BeautifulSoup(url_text, 'lxml')
        url_table = url_soup.find_all('table').pop()
        trs = url_table.find_all('tr')[1:]

        return trs
    else:
        return response.status_code


def process_data(trs):
    # process data
    content = []

    for tr in trs:
        elements = re.findall(r'<span[^>]*?>(.*?)</span>', str(tr))

        row, column = int(elements[0]), int(elements[2])
        pattern = elements[1]
        if row + 1 > len(content):
            content.extend([[] for _ in range(row + 1 - len(content))])
        if column + 1 > len(content[row]):
            content[row] += [' '] * (column + 1 - len(content[row]))
        content[row][column] = pattern
    
    return content


def display_letters(patterns: list):
    display = []

    while [] in patterns:
        empty_index = patterns.index([])

        rows, columns = empty_index, -1
        for r in range(rows):
            columns = max(columns, len(patterns[r]))

        for i in range(columns - 1, -1, -1):
            for j in range(rows):
                if i < len(patterns[j]):
                    print(patterns[j][i], end='')
                else:
                    print(' ', end='')
            print()
        print()
        
        patterns = patterns[empty_index + 1:]
    
    return True


def decryption_googledoc(url: str):
    trs = request_url(url)

    if not isinstance(trs, int):
        patterns = process_data(trs)

        return display_letters(patterns)
    else:
        return False


if __name__ == "__main__":
    # url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
    url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

    decryption_instance = decryption_googledoc(url)
