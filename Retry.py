import os.path
import proxy_extract
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    location = []
    All_Facilities = []
    Description = []

    Builder_Name = []
    Building_Name = []

    property_data = []
    location_advantages = []

    proxies = proxy_mesh()
    counter = 0
    # Detail Page -Link start
    proxy_counter = 0
    index_proxy = 0
    property_data_list = []
    for link in links:
        if proxy_counter == 9:
            proxy_counter = 0
            index_proxy += 1

        counter += 1
        print(f'We are on Link{counter}')
        global request
        session = requests.Session()
        # if request>=2:
        #     print("Sleeping for 2 sec......")
        #     time.sleep(2)
        #     request=0
        try:
            print(link)
            page = session.get(link, headers=headers, proxies={'http': proxies[index_proxy]})
            proxy_counter += 1
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            request += 1
            property_info = {
                "Rating": Placeholder,
                "BHK Types": [],
                "Property Types": [],
                "Area Ranges (sq.ft.)": [],
                "Price Ranges (Cr)": [],
                "Additional Charges": [],
                "Construction Status": [],
                "Completion Date": []
            }

            # Rating by Features- Property Data
            try:
                rating = [i.text for i in dpageSoup.select_one('div.review__rightSide>div>ul>li>div').select(
                    'div.ratingByFeature__circleWrap')]
            except AttributeError:
                rating = None
            property_info["Rating"] = rating

            # Price Information BHK wise-Property Info->Property data
            all_id = ['1_1', '1_2', '1_3', '1_4', '1_5']
            for id in all_id:
                soup = dpageSoup.find('div', id=id)
                try:
                    bhk_type = soup.select_one('.configurationCards__configBandLabel').text.strip()
                except AttributeError:
                    bhk_type = Placeholder
                try:
                    property_type = soup.select_one('.configurationCards__configBandHeading').text.strip()
                except AttributeError:
                    property_type = Placeholder
                try:
                    area_range_text = soup.select_one('.configurationCards__cardAreaSubHeadingOne').text.strip()
                except AttributeError:
                    area_range_text = Placeholder
                try:
                    price_range_text = soup.select_one('.configurationCards__cardPriceHeading').text.strip()
                except AttributeError:
                    price_range_text = Placeholder
                try:
                    additional_charges_element = soup.select_one('.configurationCards__adtnCharges')
                    additional_charges = additional_charges_element.text.strip(
                        '+ ').strip() if additional_charges_element else Placeholder
                except AttributeError:
                    additional_charges = Placeholder

                property_info["BHK Types"].append(bhk_type)
                property_info["Property Types"].append(property_type)
                property_info["Area Ranges (sq.ft.)"].append(area_range_text)
                property_info["Price Ranges (Cr)"].append(price_range_text)
                property_info["Additional Charges"].append(additional_charges)

            # Construction Status-property info-> Property Data

            # Find the div with class ConstructionStatus__collapsedCard
            construction_status_div = dpageSoup.find('div', class_='ConstructionStatus__collapsedCard')

            # Initialize construction status and completion date with Placeholder
            construction_status = Placeholder
            completion_date = Placeholder

            try:
                # Extract construction status and completion date if the div is found
                construction_status_element = construction_status_div.select_one('.ConstructionStatus__phaseStatus')
                completion_date_element = construction_status_div.select_one(
                    '.ConstructionStatus__phaseStatusSubtitle')

                construction_status = construction_status_element.text.strip() if construction_status_element else Placeholder
                completion_date = completion_date_element.text.strip() if completion_date_element else Placeholder

            except Exception as e:
                # print(f"An error occurred while extracting construction status and completion date: {e}")
                pass

                # Continue with Placeholder values

            # Add construction status and completion date to the property_data dictionary
            property_info["Construction Status"].append(construction_status)
            property_info["Completion Date"].append(completion_date)

            property_data.append(property_info)

            # Facilities- All_Facilities
            try:
                Facility_info = dpageSoup.find_all('div', class_='UniquesFacilities__xidFacilitiesCard')
                Facilities = [i.text.strip() for i in Facility_info]
            except:
                Facilities = Placeholder
            All_Facilities.append(Facilities)

            # Builder Info

            # try:
            #   Builder_info=dpageSoup.find('div',class_="ProectInfo__imgBox1 title_bold").text.strip()
            # except:
            #   Builder_info=Placeholder

            # Outer Details- location and Building_Name
            try:
                Outer_Details = dpageSoup.find('h1', class_='ProjectInfo__imgBox1 title_bold')
                location_text = Outer_Details.find('span', class_='ProjectInfo__hideTxt').text.strip()
                building_name = Outer_Details.contents[0].text.strip()
            except AttributeError:
                # Handle the exception if any of the elements are not found
                location_text = Placeholder
                building_name = Placeholder

            location.append(location_text)
            Building_Name.append(building_name)

            # Extracting project details - property_data
            try:
                project_details_div = dpageSoup.find('div',
                                                     class_='AboutProjectDetail__specTable caption_strong_medium font_family')
                project_details_table = project_details_div.find('table', class_='AboutProjectDetail__specificTable')
                rows = project_details_table.find_all('tr')

                # Create a new dictionary for project details
                project_details = {key: Placeholder for key in
                                   ["Towers", "Floors", "Units", "Total Project Area", "Open Area"]}

                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        key = columns[0].text.strip()
                        value = columns[1].text.strip()
                        project_details[key] = value
            except AttributeError:
                # Handle the exception if the specified elements are not found
                project_details = {key: Placeholder for key in
                                   ["Towers", "Floors", "Units", "Total Project Area", "Open Area"]}

            # Append project details to the DataFrame
            property_data.append(project_details)

            # Builder Name- Builder_Name
            try:
                name = dpageSoup.find('div', class_='section_header_bold spacer4').text.strip()
            except:
                name = Placeholder
            Builder_Name.append(name)

            # Nearby Locations-location_advantages

            # Loop through each div tag and extract Location and Time
            for loc in dpageSoup.find_all('div', class_='locAdvantageCarousel__locAdBoxDesktop ellipsis'):
                try:
                    name = loc.find('div', class_='list_header_semiBold').text.strip()
                except AttributeError:
                    name = Placeholder  # Handle if name is not found
                try:
                    number = loc.find('div', class_='caption_subdued_medium').text.strip()
                except AttributeError:
                    number = Placeholder  # Handle if number is not found

                # Create a dictionary and append to the list
                location_dict = {
                    "Location_Near": name,
                    "Time_taken": number
                }
                location_advantages.append(location_dict)

            # Description-Description of each link
            try:
                Description.append(dpageSoup.find('div', {'data-label': 'PROJ_DESC'}).text.strip())
            except:
                Description.append(Placeholder)
            # print(Description,location_advantages)

            # print(f'We are currently at: {} link')
            # List of lists to iterate through
            lists_to_iterate = [All_Facilities.copy(), location.copy(), Building_Name.copy(), Builder_Name.copy(), location_advantages.copy(),
                                Description.copy(), property_data.copy()]
            # Iterate through the lists and create property dictionaries
            for data_points in zip(*lists_to_iterate):
                print(data_points[0])
                print(data_points[4])
                property_dict = {
                    "All Facilities": data_points[0],
                    "Location": data_points[1],
                    "Building Name": data_points[2],
                    "Builder Name": data_points[3],
                    "Location Advantages": data_points[4],
                    "Description": data_points[5],
                    'Property Data': data_points[6]
                }
                property_data_list.append(property_dict)




        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 417:
                print(f"HTTP Error: {errh}")
                break

        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")

        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")


        except Exception as e:
            print(f"Error occurred:{e}")
        # print(property_data_list)
    to_csv(property_data_list)


def to_csv(data_list):
    # Create a DataFrame from the list of dictionaries
    Main = pd.DataFrame(data_list)

    # Write the updated Main DataFrame to the CSV file
    Main.to_csv("Full_Data2.csv", index=False)


if __name__ == '__main__':
    file = input('Enter the location of the file where you stored the urls in txt\n')
    if os.path.exists(file):
        with open(file, 'r') as f:
            urls = [line.strip() for line in f.readlines()]
        property_data_list = get_data(urls)
