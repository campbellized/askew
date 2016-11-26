"""Askew is an image viewer that searches for images and displays the results
as ASCII art.

Usage
-----
    $ python askew.py
"""

from bs4 import BeautifulSoup

import imgscii
import requests
import re
from os import path

DATA_PATH = "tmp" + path.sep


def main():
    """Retrieve images based upon user queries and view them as ASCII art."""

    while True:
        img_list = new_query()
        images = retrieve_images(img_list)

        idx = 0

        while True:
            print(images[idx])
            action = input("[N] Next | [P] Previous | [Q] Query | [X] Exit\n")
            action = action.lower()

            if action == "n" or action == "next":
                idx = file_increment(images, idx)
            elif action == "p" or action == "previous" or action == "prev":
                idx = file_decrement(images, idx)
            elif action == "q" or action == "query":
                break
            elif action == "x" or action == "exit":
                print("Bye bye.")
                exit()
            else:
                print("'" + action + "' is not a valid command.")


def file_increment(file_list, index):
    """Increment the file index by 1, accounting for rollover.

    Parameters
    ---
    file_list: list
    index: int

    Returns
    ---
    int
    """

    index += 1

    if index > len(file_list) - 1:
        return 0
    else:
        return index


def file_decrement(file_list, index):
    """Decrement the file index by 1, accounting for rollover.

    Parameters
    ---
    file_list: list
    index: int

    Returns
    ---
    int
    """

    index -= 1

    if index < 0:
        return len(file_list) - 1
    else:
        return index


def new_query():
    """Get a search term from the user and parse the site for images based on
    the user's query.

    Parameters
    ---
    None

    Returns
    ---
    object
        A BeautifulSoup object
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

    response = requests.get(url)
    data = response.text

    soup = BeautifulSoup(data, "html.parser")

    return soup.select("#downloads img")


def retrieve_images(images):
    """Download a list of images to the temp directory to be viewed

    Parameters
    ---
    images: object

    Returns
    ---
    files: list
    """

    # List of file names retrieved from query
    files = []

    for img in images[:11]:
        img_src = img.get("src")
        res = requests.get(img_src, stream=True)
        file_name = img_src.split("/")[-1]
        files.append(file_name)

        if res.status_code == 200:
            print("success")
            with open(DATA_PATH + file_name, 'wb') as file:
                file.write(res.content)

    return files


def filter_input(query):
    """Takes a string and prepares it to be used in a web query

    Parameters
    ---
    query: string

    Returns
    ---
    string
    """

    return re.sub(r"\s+", "+", query)


if __name__ == "__main__":
    main()
