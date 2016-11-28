"""Askew is an image viewer that searches for images and displays the results
as ASCII art.

Usage
-----
    $ python askew.py
"""

import re
import shutil
import errno
import os
from os import path

from bs4 import BeautifulSoup
import imgscii
import requests

TEMP_PATH = "tmp" + path.sep


def main():
    """Retrieve images based upon user queries and view them as ASCII art."""

    create_temp(TEMP_PATH) # Directory where Images are temporarily saved.

    while True:
        # Define search term and get the results of that search
        img_list = new_query()
        images = retrieve_images(img_list)

        if len(images) == 0:
            print("No images were found.")
            continue

        idx = 0

        while True:
            # Print ASCII and prompt user for action
            imgscii.printscii(TEMP_PATH + images[idx])
            action = input("[N] Next | [P] Previous | [Q] Query | [X] Exit\n")
            action = action.lower()

            if action == "n" or action == "next":
                idx = update_list_index(images, idx, 1) # Next item in list
            elif action == "p" or action == "previous" or action == "prev":
                idx = update_list_index(images, idx, -1) # Prev item in list
            elif action == "q" or action == "query":
                break
            elif action == "x" or action == "exit":
                print("Bye bye.")
                purge_temp(TEMP_PATH)
                exit()
            else:
                print("'" + action + "' is not a valid command.")
            print(idx)


def update_list_index(file_list, index, amount):
    """Increment the file index by a specified amount, accounting for rollover.

    Parameters
    ---
    file_list: list
    index: int
    amount: int

    Returns
    ---
    int
    """
    print("{} + {} = {}".format(index, amount, (index + amount)))
    index += amount
    return index % len(file_list)


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

    while True:
        query = input("What is your query?\n")

        if str(query):
            break
        else:
            print("Please enter a valid string")

    query = filter_input(query)
    url = "http://www.deviantart.com/browse/all/?section=&global=1&q=" + query
    response = requests.get(url)
    data = response.text

    soup = BeautifulSoup(data, "html.parser")

    return soup.select("#browse-results .torpedo-thumb-link > img")


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

    for img in images[:6]:
        img_src = img.get("src")
        res = requests.get(img_src)
        file_name = img_src.split("/")[-1]
        files.append(file_name)

        if res.status_code == 200:
            with open(TEMP_PATH + file_name, 'wb') as file:
                file.write(res.content)
        else:
            print("Response code: " +
                  res.status_code +
                  " - There was a problem downloading the image.")

    return files


def purge_temp(directory):
    """Delete any temporary files."""

    shutil.rmtree(directory)


def create_temp(directory):
    """Create the temp directory if it does not exist."""

    try:
        os.makedirs(directory)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


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
