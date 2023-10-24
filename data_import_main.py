import os
import proxy_extract
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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


def get_data(links):
    """Uses Default Proxy Mesh which is provided (300 proxies every 10 min)
    Input the Links in here for the url of the page you want to scrape and it will give you the page content in JSON"""
    proxies = proxy_mesh()
    counter = 0
    # Detail Page -Link start
    proxy_counter = 0
    index_proxy = 0
    property_data_list = []
    if os.path.isfile(f'{os.getcwd()}/Miscellaneous/data_import.txt'):
        with open(f'{os.getcwd()}/Miscellaneous/data_import.txt', 'r') as file2:
            start = int(file2.read())
    else:
        start = 0
    for link in range(start, len(links)):
        if proxy_counter == 9:
            proxy_counter = 0
            index_proxy += 1

        counter += 1
        print(f'We are on Link{link}')
        global request
        session = requests.Session()
        try:
            print(links[link])

            page = session.get(links[link], headers=headers, proxies={'http': proxies[index_proxy]})
            # time.sleep(2)
            print(page.status_code)
            if page.status_code == 404:  # handles Missing pages
                continue
            if page.status_code == 417:
                print('Handle the proxy')  # handle captcha or change proxy

            proxy_counter += 1
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            request += 1
            try:
                # price Range
                price = dpageSoup.select_one('#pdPrice2').text.strip()
            except Exception as e:
                price = Placeholder
                print(f'error-> {e}')

            # Area
            try:
                area = dpageSoup.select_one('#srp_tuple_price_per_unit_area').text.strip()
            except:
                area = Placeholder
            # Area with Type
            try:
                areaWithType = dpageSoup.select_one('#factArea').text.strip()
            except:
                areaWithType = Placeholder

            # Configuration
            try:
                bedRoom = dpageSoup.select_one('#bedRoomNum').text.strip()
            except:
                bedRoom = Placeholder
            try:
                bathroom = dpageSoup.select_one('#bathroomNum').text.strip()
            except:
                bathroom = Placeholder
            try:
                balcony = dpageSoup.select_one('#balconyNum').text.strip()
            except:
                balcony = Placeholder

            try:
                additionalRoom = dpageSoup.select_one('#additionalRooms').text.strip()
            except:
                additionalRoom = Placeholder

            # Address

            try:
                address = dpageSoup.select_one('#address').text.strip()
            except:
                address = Placeholder
            # Floor Number
            try:
                floorNum = dpageSoup.select_one('#floorNumLabel').text.strip()
            except:
                floorNum = Placeholder

            try:
                facing = dpageSoup.select_one('#facingLabel').text.strip()
            except:
                facing = Placeholder

            try:
                agePossession = dpageSoup.select_one('#agePossessionLbl').text.strip()
            except:
                agePossession = Placeholder

            # Nearby Locations

            try:
                nearbyLocations = [i.text.strip() for i in
                                   dpageSoup.select_one('div.NearByLocation__tagWrap').select(
                                       'span.NearByLocation__infoText')]
            except:
                nearbyLocations = Placeholder

            # Descriptions
            try:
                description = dpageSoup.select_one('#description').text.strip()
            except:
                description = Placeholder

            # Furnish Details
            try:
                furnishDetails = [i.text.strip() for i in dpageSoup.select_one('#FurnishDetails').select('li')]
            except:
                furnishDetails = Placeholder

            # Features
            if furnishDetails:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[1].select('li')]
                    print(features)
                except:
                    features = Placeholder
            else:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[0].select('li')]
                except:
                    features = Placeholder

            # Rating by Features
            try:
                rating = [i.text for i in dpageSoup.select_one('div.review__rightSide>div>ul>li>div').select(
                    'div.ratingByFeature__circleWrap')]
            except:
                rating = Placeholder
            # print(top_f)

            try:
                # Property ID
                property_id = dpageSoup.select_one('#Prop_Id').text.strip()
            except:
                property_id = Placeholder

            try:
                # More_description
                more_describe = dpageSoup.select_one('#AboutPropertyComponent').text.strip()
            except:
                more_describe = Placeholder
            # print(more_describe)

            try:
                # additional_info
                additional_info = dpageSoup.select_one("#AdditionalDetailsComponent").text.strip()
            except:
                additional_info = Placeholder
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

            # property_data_list.append(property_data)
            print(property_data['price'])
            if not (property_data['price']):

                with open(fr'{os.getcwd()}/Miscellaneous/data_import.txt', 'w') as file1:
                    file1.write(str(link))
                # Added a recursion so that we don't have to restart again and again
                print('Please verify captcha on link -> {}'.format(links[link]))
                time.sleep(10)
                if os.path.exists(file):
                    with open(file, 'r') as f:
                        urls = [line.strip() for line in f.readlines()]
                    property_data_list = get_data(urls)

            if os.path.isfile('data_import.json'):
                with open('data_import.json', 'r') as json_file:
                    existing_data = json.load(json_file)

            else:
                existing_data = []

            # I now want to merge the elements in property data list to existing data
            existing_data.append(property_data)
            updated_json_data = json.dumps(existing_data, indent=4)

            # Write the updated JSON data back to the file
            with open('data_import.json', 'w') as json_file:
                json_file.write(updated_json_data)

            print('New data has been added to data_import.json')

        except Exception as e:
            print(f"Error occurred:{e}")
            sys.exit()

    return property_data_list


if __name__ == '__main__':
    file = input('Enter the location of the file where you stored the urls in txt\n')
    if os.path.exists(file):
        with open(file, 'r') as f:
            urls = [line.strip() for line in f.readlines()]
        property_data_list = get_data(urls)

        full_data = pd.DataFrame()
        for property_data_l in property_data_list:
            p = pd.DataFrame(property_data_l)
            full_data = pd.concat([full_data, p], ignore_index=True)
        full_data.to_csv('Full_data.csv')
        print('Data has been written to Full_data.csv')
    else:
        print('Wrong path')
