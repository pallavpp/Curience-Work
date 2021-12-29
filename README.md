# Curience-Work
Pallav and Alokeveer's Work.

## Info
- Scraping and filtering scripts present in `Scripts` folder.
- Custom modules are present in `Modules` folder.
- Scraped and filtered data is saved in CSV format in `Data` folder. Scripts automatically save to Data folder.
- Files containing reading data are present in `Read_Files` folder.
- Add following code to scripts to import custom modules:
```
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
```
- Before running scripts that use selenium, user will have to update driver path in script.
- `Scripts/final_data.py` will filter all CSV files present in `Data`, based on keywords present in `Read_Files/keywords.txt`, and store the combined data in a CSV file inside `Data`.
    - ***Each line in `Read_Files/keywords.txt` is treated as a keyword.***
    - For all scraping scripts, use the following column names only: ["Blog Category", “Blog Title”, “Blog Date”, "Blog Catchphrase", “Blog Link”, “Author Name”, “Author Profile Link”, “Thumbnail Link”, “Thumbnail Credit”]. ***If you decide to include any new column name not listed here, update the above list so others know to use it in the future. If not done, filtered data may contain redundant columns.***

## All Requirements
- [Selenium](https://pypi.org/project/selenium/)
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [Requests](https://pypi.org/project/requests/)
- [lxml](https://pypi.org/project/lxml/)
- [dataclasses](https://pypi.org/project/dataclasses/)
