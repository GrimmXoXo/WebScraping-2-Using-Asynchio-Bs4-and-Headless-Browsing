from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
from webdriver_manager.chrome import ChromeDriverManager


def extract(url):
    '''Enter the URL for Json'''
    # Use ChromeDriverManager to download and manage the Chrome WebDriver
    service = Service(ChromeDriverManager().install())

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36')  # Such that we behave like actual person

    driver = webdriver.Chrome(service=service,
                              options=chrome_options)  # Now we can use 'driver' to interact with the web page


    driver.get(url)

    # time.sleep(5) #Just incase we want to delay for page to render

    # Get the WebElement containing the JSON content
    json_element = driver.find_element(by=By.XPATH, value='/html/body')

    # Get the text content of the WebElement
    json_content = json_element.text

    # Parse the JSON content
    json_data = json.loads(json_content)

    return json_data

def extract_all_url(city=12):
    '''It extracts all the URL from the JSON of the site. Give the city number which you want to extract; check that in the site, you can find them in the network tab.'''
    all_url = []

    for page in range(1, 2589):
        print(f'we are on page {page}')
        json_url = f"https://www.99acres.com/api-aggregator/discovery/srp/search?area_unit=1&platform=DESKTOP&moduleName=GRAILS_SRP&workflow=GRAILS_SRP&page_size=25&page={page}&city={city}&preference=S&res_com=R&seoUrlType=DEFAULT&recomGroupType=VSP&pageName=SRP&groupByConfigurations=true&lazy=true"
        a = extract(json_url)

    try:
        for i in range(len(a['properties'])):
            try:
                b = 'https://www.99acres.com/' + a['properties'][i]['PROP_DETAILS_URL']
                all_url.append(b)
            except KeyError:
                try:
                    b = a['properties'][i]['landingPage']['url']
                    all_url.append(b)
                except KeyError:
                    # Handle the situation where 'landingPage' key or 'url' key does not exist
                    # You can raise a custom exception, log a message, or perform any other appropriate action.
                    print("Error: 'landingPage' or 'url' key not found.")
                    continue
    except Exception as e:
        print(f"Error occurred: {e}")
    # Handle other exceptions here if needed


    print("Extraction completed.")
    return all_url





if __name__=='__main__':
    e=extract_all_url()
    with open('all_url.txt','w') as file:
        for i in e:
            file.write(i+'\n')

