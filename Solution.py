import time

import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_solution(url: str):

    driver = webdriver.Chrome()
    url1 = url.replace('viewsolution', 'viewplaintext')
    driver.get(url1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('pre')[0].text
    driver.close()
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find_all('a', {'class': '_link_1xoi8_21'})[2]
    problem_code = link.text
    link = link['href']

    # print(soup)
    spans = soup.find_all('span')
    lang = soup.find_all('div', {'class': '_ideLanguageName_1jy8z_268'})[0].text.split(':')[1].strip(' ')
    memory = spans[334].text
    status = spans[329].text


    rows = soup.find_all('td')

    min_time = 100

    for row in rows:
        if 'Correct' in row.text and '-' not in row.text:

            times = float(row.text.split('(')[1].split(')')[0])
            if (times < min_time):
                min_time = times



    driver.close()

    filename = problem_code + language_extensions[lang]
    with open(filename , 'w') as f:
        f.write(data)
        f.write('\n')
    # with open('README.md', 'w') as f:
    #     f.write(f'## Problem Code: {problem_code}\n')
    #     f.write(f'## Status: {status}\n')
    #     f.write(f'## Memory: {memory}\n')
    #     f.write(f'## Time: {time}\n')
    #     f.write(f'## Link: {link}\n')
    #     f.write(f'## Language: {lang}\n')
    #     f.write('## Solution:\n')

    return filename,data







language_extensions = {
    "Python3": ".py",
    "Java": ".java",
    "C++14": ".cpp",
    "C": ".c",
    "C++17": ".cpp",
    "C++20": ".cpp",
    "C#": ".cs",
    "PyPy 3": ".py",
    "Pyscript": ".py",
    "R": ".r",
    "OracleDB": ".sql",
    "Rust": ".rs",
    "Kotlin": ".kt",
    "Go": ".go",
    "JavaScript": ".js",
    "HTML": ".html",
    "CSS": ".css",
    "PHP": ".php",
    "SQL": ".sql",
}

