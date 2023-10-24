# WebScraping-2: Using Asynchio, BeautifulSoup, and Headless Browsing

This repository contains scripts for web scraping using asynchronous programming (Asynchio), BeautifulSoup (Bs4), and headless browsing techniques. The scripts enable efficient extraction of data from websites, handling IP bans, error 404s, and proxy rotations.

## Files Description

### 1. `json_extract.py`

This script allows you to extract URLs from JSON pages based on the city and page number. It uses a headless browser and proxies. Extracted URLs are stored in a text file.

### 2. `json_extract_asynch.py`

Similar to `json_extract.py`, this script performs the same task using asynchronous programming, allowing for parallelization and faster data extraction. Note that it may encounter errors if the rate limit exceeds or if public proxies are insufficient.

### 3. `data_import_main.py`

This file extracts information from HTML pages using BeautifulSoup and class IDs. It handles IP bans by rotating proxies and automatically handles 404 errors by moving to the next page.

### 4. `data_import_asynchio.py`

Synchronous counterpart of `data_import_main.py` with similar functionalities and restrictions as `json_extract_asynch.py`.

### 5. `data_import_second.py`

Used for extracting pages that do not follow the pattern with ID selectors. It uses XPath for extraction.

### 6. `proxy_extract.py`

This script extracts 300 proxies available for free on a proxy website and provides them as a dictionary for use in the data import or JSON extraction files.

## Usage

1. **Setting Up Proxies and Headless Browsing:**
   - Ensure you have a list of proxies or use `proxy_extract.py` to obtain them.
   - Configure headless browsing and proxy settings in the scripts as needed.

2. **Running the Scripts:**
   - Run the appropriate script based on your scraping requirements.
   - Adjust the parameters like city, page number, etc., within the scripts as necessary.

3. **Handling Errors and Restrictions:**
   - For IP bans, consider using paid proxies or a VPN and implement rotation.
   - For error 404, the scripts are designed to automatically move to the next page.
   - For advanced challenges like Captcha verification, implement automation techniques based on your needs.

## Note

- Ensure you comply with the website's terms of service and legal regulations while scraping.
- Regularly check and update the list of proxies for optimal performance.

Feel free to contribute, report issues, or provide suggestions to improve the functionality and efficiency of these scripts.

Happy Scraping!
