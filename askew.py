"""Askew is an image viewer that searches for images and displays the results
as ASCII art.

Usage
-----
    $ python askew.py
"""

from bs4 import BeautifulSoup

import requests
import re

DATA_PATH = "tmp/"


def main():
    """This is a placeholder.
    """

    # while True:
    #     query = input("What is your query?\n")
    #
    #     if str(query):
    #         break
    #     else:
    #         print("Please enter a valid string")
    #
    # query = filter_input(query)
    # url = "http://www.deviantart.com/browse/all/?section=&global=1&q=" + query
    url = "http://www.campbellized.com/"
    print(url)
    r = requests.get(url)
    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    img_list = soup.select("#downloads img")
    log = ""

    for img in img_list[:11]:
        img_src = img.get("src")
        log += img_src + "\n"
        res = requests.get(img_src, stream=True)
        file_name = img_src.split("/")[-1]

        if res.status_code == 200:
            print("success")
            with open(DATA_PATH + file_name, 'wb') as file:
                file.write(res.content)

    with open(DATA_PATH + "src.txt", "w") as text_file:
        text_file.write(log)


def filter_input(query):
    """Takes a string and prepares it to be used in a web query
    """

    return re.sub("\s+", "+", query)


if __name__ == "__main__":
    main()
