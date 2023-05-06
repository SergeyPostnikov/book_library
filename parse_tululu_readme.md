#### parising by diapason ids

*   Navigate to the project directory in a terminal
*   Run the following command:

```
python parse_tululu_by_id.py --start_id 1 --end_id 10
```
*   Replace the start\_id and end\_id arguments with the desired range of ids to download

#### parising by diapason pages
for download around 100 book and render pages for review them on page you should type: 
```
python parse_tululu_category.py --start_page 1 --end_page 4
```
then, in directory `pages` will appear html files with your books.

![pages](https://user-images.githubusercontent.com/60840361/236615737-342cd090-e085-4ebb-b3a6-034930a41b41.jpg)


if you open them by your browser, appear possibility to observe titles, authors and click for read books.
![page](https://user-images.githubusercontent.com/60840361/236615903-fa7d9807-ac08-4995-9013-11c2bacda308.jpg)


# additional arguments

- `--start_page` - Nubmer of page for the start parsing.

- `--end_page` - Nubmer of page for the stop parsing

- `--dest_folder` - path, to books directory.
  * by default `books` in project folder.
  
- `--skip_imgs` -  skip downloading image of book.

- `--skip_txt` - skip downloading text of book.

- `--json_path` - location of library.json
  * by default located in project folder
