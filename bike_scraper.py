import requests
from bs4 import BeautifulSoup

url = "https://pogoh.com/system-map/"


def scrape_bike_data():
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to fetch the page:", response.status_code)

    soup = BeautifulSoup(html_content, "lxml")
    station_list = soup.find("ul", id="infoWind")
    stations = []
    for li in station_list.find_all("li"):
        name = li.find("h5").text
        available_bikes = int(
            li.find_all("div", class_="infotxt")[0].find("strong").text
        )
        empty_docks = int(li.find_all("div", class_="infotxt")[1].find("strong").text)

        stations.append(
            {
                "name": name,
                "available_bikes": available_bikes,
                "empty_docks": empty_docks,
            }
        )

    for station in stations:
        print(station)


if __name__ == "__main__":
    scrape_bike_data()
