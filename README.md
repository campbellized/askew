# Askew - ASCII Image Viewer
Askew is a command-line program that lets you view images from DeviantArt as ASCII images.

## Requirements

Askew requires [Imgscii](https://github.com/campbellized/imgscii) (another one of my projects) as well as a couple other packages. You can install them using PIP:
```
pip install imgscii
pip install beautifulsoup4
pip install requests
```
Please note, Askew has only been tested in Python 3.

## Getting started
To get started all you need to do is run `python askew.py` from the command-line.
```
python askew.py
```
After that, all you have to do is specify a query and view the results. Queries will return the first five results and you need to wait at least 10 seconds between queries.
