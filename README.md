# Curience-Work
Pallav and Alokeveer's Work

## Info
- Site specific scraping scripts present in `Scripts` directory.
- Custom modules are present in `Modules` directory.
- Scraped data is saved in CSV format in `Data` directory. Scripts automatically save CSV in Data folder.
- For scripts usign selenium, user will have to update driver path in script before executing.
- Add following code to scripts to import custom modules:
```
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
```

## All Requirements
- [Selenium](https://pypi.org/project/selenium/)
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [Requests](https://pypi.org/project/requests/)
- [lxml](https://pypi.org/project/lxml/)
- [dataclasses](https://pypi.org/project/dataclasses/)
