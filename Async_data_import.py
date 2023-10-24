import os.path
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd
import proxy_extract
location = []
from aiohttp_proxy import ProxyConnector,ProxyType

All_Facilities = []
Area = []
Address = []
NearbyLocations = []
Description = []
Features = []
Builder_Name = []
Building_Name = []
Rating = []
Property_id = []
property_data = []
location_advantages = []
project_details = {}
request = 0
Placeholder = None
import time

headers = {
    'authority': 'www.99acres.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="107", "Not;A=Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'Expect': '',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/527.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

def proxy_mesh():
    proxies = proxy_extract._extract_proxies_free_proxy_list_net()
    P_300 = []
    for proxy_obj in proxies:

        if proxy_obj['https'] == 'yes':
            proxy_obj['protocol'] = 'https'
        else:
            proxy_obj['protocol'] = 'http'
        proxy = f"{proxy_obj['protocol']}://{proxy_obj['ip']}:{proxy_obj['port']}"
        P_300.append(proxy)
    return P_300


async def fetch_data(link,proxy):

    global request
    property_data_list = []

    async with aiohttp.ClientSession(headers=headers,trust_env = True) as session:

        async with session.get(link, headers=headers,proxy=proxy) as response:
            html_content = await response.text()
            dpageSoup = BeautifulSoup(html_content, 'html.parser')
            request += 1
            try:
                # price Range
                price = dpageSoup.select_one('#pdPrice2').text.strip()
            except Exception as e:
                price = ''
                # print(e)

            # Area
            try:
                area = dpageSoup.select_one('#srp_tuple_price_per_unit_area').text.strip()
            except:
                area = ''
            # Area with Type
            try:
                areaWithType = dpageSoup.select_one('#factArea').text.strip()
            except Exception as e:
                areaWithType = ''
                # print(e)

            # Configuration
            try:
                bedRoom = dpageSoup.select_one('#bedRoomNum').text.strip()
            except:
                bedRoom = ''
            try:
                bathroom = dpageSoup.select_one('#bathroomNum').text.strip()
            except:
                bathroom = ''
            try:
                balcony = dpageSoup.select_one('#balconyNum').text.strip()
            except:
                balcony = ''

            try:
                additionalRoom = dpageSoup.select_one('#additionalRooms').text.strip()
            except:
                additionalRoom = ''

            # Address

            try:
                address = dpageSoup.select_one('#address').text.strip()
            except:
                address = ''
            # Floor Number
            try:
                floorNum = dpageSoup.select_one('#floorNumLabel').text.strip()
            except:
                floorNum = ''

            try:
                facing = dpageSoup.select_one('#facingLabel').text.strip()
            except:
                facing = ''

            try:
                agePossession = dpageSoup.select_one('#agePossessionLbl').text.strip()
            except:
                agePossession = ''

            # Nearby Locations

            try:
                nearbyLocations = [i.text.strip() for i in
                                   dpageSoup.select_one('div.NearByLocation__tagWrap').select(
                                       'span.NearByLocation__infoText')]
            except:
                nearbyLocations = ''

            # Descriptions
            try:
                description = dpageSoup.select_one('#description').text.strip()
            except:
                description = ''

            # Furnish Details
            try:
                furnishDetails = [i.text.strip() for i in dpageSoup.select_one('#FurnishDetails').select('li')]
            except:
                furnishDetails = ''

            # Features
            if furnishDetails:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[1].select('li')]
                except:
                    features = ''
            else:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[0].select('li')]
                except:
                    features = ''

            # Rating by Features
            try:
                rating = [i.text for i in dpageSoup.select_one('div.review__rightSide>div>ul>li>div').select(
                    'div.ratingByFeature__circleWrap')]
            except:
                rating = ''
            # print(top_f)

            try:
                # Property ID
                property_id = dpageSoup.select_one('#Prop_Id').text.strip()
            except:
                property_id = ''

            try:
                # More_description
                more_describe = dpageSoup.select_one('#AboutPropertyComponent').text.strip()
            except:
                more_describe = ''
            # print(more_describe)

            try:
                # additional_info
                additional_info = dpageSoup.select_one("#AdditionalDetailsComponent").text.strip()
            except:
                additional_info = ''
            # print(additional_info)

            # Create a dictionary with the given variables
            property_data = {
                'price': price,
                'area': area,
                'areaWithType': areaWithType,
                'bedRoom': bedRoom,
                'bathroom': bathroom,
                'balcony': balcony,
                'additionalRoom': additionalRoom,
                'address': address,
                'floorNum': floorNum,
                'facing': facing,
                'agePossession': agePossession,
                'nearbyLocations': nearbyLocations,
                'description': description,
                'More Description': more_describe,
                'furnishDetails': furnishDetails,
                'features': features,
                'rating': rating,
                'property_id': property_id,
                'additional_info': additional_info
            }

            property_data_list.append(property_data)
            print(property_data_list)


async def get_data_async(urls, uses_per_proxy=900,Proxy_list):
        """ Urls: list of urls which you want to scrape
            uses_per_proxy: DEFAULT=900; this means that from the list of proxies, how many times do you need to use 1 proxy
            Example if total proxies you can get in proxy mesh
            Proxy_list: Send the list of proxies which you are using, I created a function named proxy mesh in which 300 proxies are stored and refreshed every 10 minutes.
            To use proxy_mesh function->
                proxy_mesh_list=proxy_mesh()
                and then pass this proxy_mesh as an argument inside this function  

            Error: Using Asynchronous Requests to speed up the process of data gathering but it didnt work because the proxies which i was trying to use to get the data were Public and limited
            The error the script is encountering is aiohttp.client_exceptions.ClientProxyConnectionError: Cannot connect to host {ip here} ssl:default [An operation on a socket could not be performed because the system lacked sufficient buffer space or because a queue was full]
            What i feel like this means either my machine didnt have the capacity to perform operations asynch(i had 70k urls) or either the new client i.e proxy was ratelimiting my access to the parallalization
            In either case we can just use the headless browser with requests and get it done albeit slow."""
    proxy_usage_counts = {proxy : uses_per_proxy for proxy in proxy_mesh_list}
    tasks = []
    # print(proxy_usage_counts['proxy'][0])
    for link in urls:
        proxy = next((proxy for proxy, uses in proxy_usage_counts.items() if uses > 0), None)
        if proxy:
            tasks.append(fetch_data(link, proxy))
            proxy_usage_counts[proxy] -= 1
        else:
            print("No available proxies.")
            break

    property_data_list = await asyncio.gather(*tasks)
    return property_data_list


if __name__ == '__main__':
    # file = input('Enter the location of the file where you stored the urls in txt\n')
    proxy_mesh_list=proxy_mesh()
    file = r"all_url.txt"
    if os.path.exists(file):
        with open(file, 'r') as f:
            urls = [line.strip() for line in f.readlines()]

    request = 0  # Initialize request count
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(get_data_async(urls,Proxy_list=proxy_mesh_list))
    loop.close()





    full_data = pd.DataFrame()
    for property_data_l in data:
        p = pd.DataFrame(property_data_l)
        print(p)
        full_data = pd.concat([full_data, p], ignore_index=True)
        full_data.to_csv('Full_data.csv')
        # print('Data has been written to Full_data.csv')
    else:
        print('Wrong path')
