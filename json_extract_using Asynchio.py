import asyncio
import aiohttp
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

async def fetch_url(session, url):
    # Asynchronously fetches JSON data from the given URL using aiohttp session
    async with session.get(url,headers=headers) as response:
        json_data = await response.json()
        return json_data


async def main(city_number=12):
    # Initialize an empty list to store extracted URLs
    all_url = []

    # Base URL for the API endpoint
    base_url = ""

    # List to store asynchronous tasks for fetching JSON data
    tasks = []

    # Create an aiohttp client session
    async with aiohttp.ClientSession() as session:
        # Iterate over a range of pages to construct JSON URLs
        for page in range(1, 2589):
            # Construct the JSON URL for the current page
            # Mumbai city number of site was 12 you can find city number by inspecting site
            json_url = f"{base_url}?area_unit=1&platform=DESKTOP&moduleName=GRAILS_SRP&workflow=GRAILS_SRP&page_size=25&page={page}&city={city_number}&preference=S&res_com=R&seoUrlType=DEFAULT&recomGroupType=VSP&pageName=SRP&groupByConfigurations=true&lazy=true"

            # Append an asynchronous task to fetch JSON data for the current URL
            tasks.append(fetch_url(session, json_url))

        # Run all asynchronous tasks concurrently and gather their results
        json_responses = await asyncio.gather(*tasks)

        # Iterate over JSON responses
        for response in json_responses:
            # Iterate over 'properties' in each JSON response (or an empty list if not present)
            for property_data in response.get('properties', []):
                try:
                    # Extract the property URL from JSON data
                    b = '' + property_data['PROP_DETAILS_URL']
                except KeyError:
                    # If the expected key is not present, extract URL from 'landingPage' or use an empty string
                    b = property_data.get('landingPage', {}).get('url', '')

                # Append the extracted URL to the list
                all_url.append(b)

    # Return the list of extracted URLs
    return all_url


# If the script is run directly (not imported as a module)
if __name__ == "__main__":
    # Run the asynchronous main function using asyncio.run()
    city = int(input('Enter City Number'))
    all_url = asyncio.run(main(city_number=city))
    # Save the list of URLs to a text file
    with open('urls.txt', 'w') as file:
        for url in all_url:
            file.write(f"{url}\n")

    print(f"All URLs have been saved to 'urls.txt'")
