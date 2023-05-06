Project Title
=============

Tululu.org books downloader, and tool for render site on you local computer.
[online version](https://sergeypostnikov.github.io/book_library/pages/index1.html)

Description
-----------

This Python script downloads books and their covers from the [Tululu.org](http://tululu.org/) website, a collection of books in Russian without registration.

The script allows to download books within a specific range of ids or for a single book by providing its id or category.

The books are downloaded in a plain text format and saved in the "books" directory. The covers are downloaded in JPG format and saved in the "images" directory.

Getting Started
---------------

### Dependencies

*   Python 3.6 or higher
*   Libraries: requests, beautifulsoup4, pathvalidate

### Installing

*   Clone the repository or download the files
*   Install the required libraries by running the following command in a terminal:


```
pip install -r requirements.txt
```

### Executing program

#### parising by diapason pages
for download around 100 book and render pages for review them on page you should type: 
```
python parse_tululu_category.py --start_page 1 --end_page 4
```
then, in directory `pages` will appear html files with your books.

![pages](https://user-images.githubusercontent.com/60840361/236615737-342cd090-e085-4ebb-b3a6-034930a41b41.jpg)


if you open them by your browser, appear possibility to observe titles, authors and click for read books.
![page](https://user-images.githubusercontent.com/60840361/236615903-fa7d9807-ac08-4995-9013-11c2bacda308.jpg)
to read more about parse_tululu_category, read the docs [here](https://github.com/SergeyPostnikov/book_library/blob/main/parse_tululu_readme.md)

#### 

