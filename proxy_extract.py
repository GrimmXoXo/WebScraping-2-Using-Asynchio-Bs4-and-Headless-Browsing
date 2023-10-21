from bs4 import BeautifulSoup
import requests
url='https://free-proxy-list.net/'
def _extract_proxies_free_proxy_list_net(https=False):
    """Function to extract proxies from https://free-proxy-list.net/
    Returns a list of proxies, params: https:default(False) Flag to check whether we only want https reqs or not"""

    proxy_list = []
    a=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46'})
    soup = BeautifulSoup(a.content, "html.parser")
    table_list = soup.select("#list > div > div.table-responsive > div > table > tbody")
    print(table_list)

    if table_list:
        table = table_list[0]
        for each_tr in table.select("tr"):
            table_td = each_tr.select("td")
            if len(table_td) > 3:
                if https == True:
                    if str(table_td[6].text.upper()) == "YES":
                        proxy = {
                            "ip": table_td[0].text,
                            "port": table_td[1].text,
                            "country": table_td[3].text,
                            "anonymity": table_td[4].text,
                            "https": table_td[6].text
                        }
                        proxy_list.append(proxy)
                else:
                    proxy = {
                        "ip": table_td[0].text,
                        "port": table_td[1].text,
                        "country": table_td[3].text,
                        "anonymity": table_td[4].text,
                        "https": table_td[6].text
                    }
                    proxy_list.append(proxy)

    return proxy_list



