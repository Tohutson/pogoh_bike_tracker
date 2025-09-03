import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://pogoh.com/system-map/"

conn = sqlite3.connect("bikeshare.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_name TEXT,
        available_bikes INTEGER,
        empty_docks INTEGER,
        last_updated DATETIME,
        UNIQUE(station_name, last_updated)
    )
    """
)
conn.commit()

response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch the page:", response.status_code)

soup = BeautifulSoup(html_content, "lxml")
station_list = soup.find("ul", id="infoWind")

for li in station_list.find_all("li"):
    station_name = li.find("h5").text

    last_updated_iso = None
    last_updated_span = li.find(
        "span", string=lambda t: t and "last updated" in t.lower()
    )
    if last_updated_span:
        time_str = last_updated_span.text.split("last updated")[-1].strip()
        time_str = time_str.replace(" PM", "").replace(" AM", "")
        parsed_time = datetime.strptime(time_str, "%H:%M:%S").time()
        last_updated_dt = datetime.combine(datetime.today().date(), parsed_time)
        last_updated_iso = last_updated_dt.strftime("%Y-%m-%d %H:%M:%S")

    infotxts = li.find_all("div", class_="infotxt")
    available_bikes, empty_docks = [int(div.find("strong").text) for div in infotxts]

    cursor.execute(
        """
        INSERT OR IGNORE INTO stations (station_name, available_bikes, empty_docks, last_updated)
        VALUES (?, ?, ?, ?)
        """,
        (station_name, available_bikes, empty_docks, last_updated_iso),
    )
    conn.commit()
