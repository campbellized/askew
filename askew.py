"""Askew is an image viewer that queries Google Images and displays the results
as ASCII art.

Usage
-----
    $ python askew.py
"""

from bs4 import BeautifulSoup

import requests
import re


def main():
    """This is a placeholder.
    """

    while True:
        query = input("What is your query?\n")

        if str(query):
            break
        else:
            print("Please enter a valid string")

    query = filter_input(query)
    url = "https://www.google.com/search?site=&tbm=isch&q=" + query
    print(url)

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")


def filter_input(query):
    """Takes a string and prepares it to be used in a web query
    """

    return re.sub("\s+", "+", query)


if __name__ == "__main__":
    main()
