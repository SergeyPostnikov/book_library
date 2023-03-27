Project Title
=============

Tululu.org books downloader

Description
-----------

This Python script downloads books and their covers from the [Tululu.org](http://tululu.org/) website, a collection of books in Russian without registration.

The script allows to download books within a specific range of ids or for a single book by providing its id.

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

*   Navigate to the project directory in a terminal
*   Run the following command:


```
python main.py --start_id 1 --end_id 10
```

*   Replace the start\_id and end\_id arguments with the desired range of ids to download
*   Alternatively, provide a single id to download a single book:

```
python main.py --start_id 1 --end_id 1
```

