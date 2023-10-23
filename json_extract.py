from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import json
import os
import sys
from webdriver_manager.chrome import ChromeDriverManager
user_agent=UserAgent()

def extract(url):
    '''Enter the URL for Json'''
    # Use ChromeDriverManager to download and manage the Chrome WebDriver
    service = Service(ChromeDriverManager().install())

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument(
        f'--user-agent={user_agent.random}')  # Such that we behave like actual person

    driver = webdriver.Chrome(service=service,
                              options=chrome_options)  # Now we can use 'driver' to interact with the web page
    driver.delete_all_cookies()
    driver.get(url)

    # time.sleep(5) #Just incase we want to delay for page to render
    # Wait for the presence of the JSON element using ExpectedConditions (maximum wait time: 10 seconds)
    json_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body'))
    )
    # Get the text content of the WebElement
    json_content = json_element.text

    # Parse the JSON content
    json_data = json.loads(json_content)

    return json_data


def extract_all_url(city=12,end_page=2837):
    """It extracts all the URL from the JSON of the site. Give the city number which you want to extract; check that in the site, you can find them in the network tab."""
    global page
    path_to_save_start=fr'{os.getcwd()}/Miscellaneous/start.txt'

    # Create the directory if it does not exist
    if not os.path.exists(path_to_save_start):
        os.makedirs(path_to_save_start)

    all_url = []
    if os.path.exists(path_to_save_start):
        with open(path_to_save_start, 'r') as f:
            start_value = int(f.read())
    else:
        start_value = 1

    for page in range(start_value, end_page):
        print(f'we are on page {page}')
        json_url = f"https://www.99acres.com/api-aggregator/discovery/srp/search?area_unit=1&platform=DESKTOP&moduleName=GRAILS_SRP&workflow=GRAILS_SRP&page_size=25&page={page}&city={city}&preference=S&res_com=R&seoUrlType=DEFAULT&recomGroupType=VSP&pageName=SRP&groupByConfigurations=true&lazy=true"
        a = extract(json_url)

        try:
            for properties_urls in range(len(a['properties'])):
                try:
                    b = 'https://www.99acres.com/' + a['properties'][properties_urls]['PROP_DETAILS_URL']
                    all_url.append(b)
                except KeyError:
                    try:
                        b = a['properties'][properties_urls]['landingPage']['url']
                        all_url.append(b)
                    except KeyError:
                        # Handle the situation where 'landingPage' key or 'url' key does not exist
                        # You can raise a custom exception, log a message, or perform any other appropriate action.
                        print("Error: 'landingPage' or 'url' key not found.")

        except Exception as e:
            print(f"Error occurred: {e}")
            with open('all_url.txt', 'a') as f:
                for m in all_url:
                    f.write(m + '\n')
            with open(path_to_save_start, 'w') as s:
                s.write(str(page))

            sys.exit()

        # Handle other exceptions here if needed

    with open('all_url.txt', 'a') as f:
        for m in all_url:
            f.write(m + '\n')
    with open(path_to_save_start, 'w') as s:
        s.write(str(page))
    return all_url


if __name__ == '__main__':
    try:
        e = extract_all_url()
        print('Execution done')
    except Exception as e:
        print(f'Error occurred {e}')

