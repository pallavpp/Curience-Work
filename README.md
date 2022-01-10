# Curience-Work
Pallav and Alokeveer's Work.

## Info
- Scraping scripts are present in `Scripts` folder.
    - Scraped data will be saved in CSV format in `Data` folder.
    - Before running scripts that use selenium, user will have to update _driver path_ in script.
    - For all scraping scripts, choose column names from the following list only: ["Blog Title", "Blog Date", "Blog Catchphrase", "Blog Category", "Blog Link", "Author Name", "Author Profile Link", "Thumbnail Link", "Thumbnail Credit"]. ***If you decide to include any new column name not listed here, update the above list so others know to use it in the future. If not done, filtered data may contain redundant columns.***
- Custom modules are present in `Modules` folder. Add following code to scripts to import custom modules:
    ```
    import os
    import sys
    modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
    if modules_path not in sys.path:
        sys.path.insert(1, modules_path)
    ```
- Files containing reading data are present in `Read_Files` folder.
    - ***Each line in Read_Files/keywords.txt is treated as a keyword.***
- `Filtered_Data` folder contains filtering scripts and sorted, cumulated and filtered data.
    - _Filtered_Data/final_data.py_ reads all CSV files from `Data` folder and filters them based on keywords read from _Read_Files/keywords.txt_. If required, user will have to update _max rows in output_ in the script.
    - Criteria used to reject poor results:
        - If year present in Blog Date - remove if < 2022, keep if 2022 present. Keywords in title increase score by 1.
        - Remove if Blog Date or Blog/Thumbnail Link non empty and contain year <  2021.
- `Analytics` folder contains document analytics.

## All Requirements
- [Selenium](https://pypi.org/project/selenium/)
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [Requests](https://pypi.org/project/requests/)
- [lxml](https://pypi.org/project/lxml/)
- [dataclasses](https://pypi.org/project/dataclasses/)
