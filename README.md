# Curience-Work
Pallav and Alokeveer's Work.

## Info
- Site specific scraping scripts present in `Scripts` directory.
- Custom modules are present in `Modules` directory.
- Scraped data is saved in CSV format in `Data` directory. Scripts automatically save CSV in Data folder.
- Add following code to scripts to import custom modules:
```
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
```
- Before running scripts that use selenium, user will have to update driver path in script.
- `Scripts/final_data.py` will filter all CSV files present in `Data` based on keywords, and store the combined data in a CSV file inside `Data`.
    - ***Keyword list present inside `Scripts/final_data.py` has to be manually updated.***
    - For all scraping scripts, use the following column names only: [“Blog Title”, “Blog Date”, “Blog Link”, “Author Name”, “Author Profile Link”, “Thumbnail Link”, “Thumbnail Credit”]. ***If you decide to include any new column name not listed here, add it to the column list present inside `Scripts/final_data.py` and update in the above list as well. If not done, the new column will not be used while filtered data.***

## All Requirements
- [Selenium](https://pypi.org/project/selenium/)
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [Requests](https://pypi.org/project/requests/)
- [lxml](https://pypi.org/project/lxml/)
- [dataclasses](https://pypi.org/project/dataclasses/)
