# Pittsburgh Bike Tracker

This project scrapes real-time data from public bike stations around **Pittsburgh** using the [Pogoh system map](https://pogoh.com/system-map/) and stores it in a local SQLite database. It tracks:

- Station name
- Number of available bikes
- Number of empty docks
- Last updated timestamp

The script is **automated to run every 30 minutes** using `cron` on a local machine.

## Features

- Scrapes station data directly from the website.
- Stores data in a SQLite database (`bikeshare.db`) with a unique constraint to avoid duplicate entries for the same timestamp.
- Uses BeautifulSoup for parsing HTML.
- Automatically timestamps each entry with today's date.

## Setup

1. Clone the repository or copy the script to your machine.
2. Make sure Python 3 and required packages are installed:

   ```bash
   pip install requests beautifulsoup4 lxml
   ```

3. (Optional) Use a virtual environment like Anaconda:

   ```bash
   conda create -n pogoh_env python=3.10
   conda activate pogoh_env
   pip install requests beautifulsoup4 lxml
   ```

## Running

Run the script manually:

```bash
python bike_scraper.py
```

Or automate using cron (every 30 minutes):

```bash
*/30 * * * * /full/path/to/python /full/path/to/your_script.py >> /full/path/to/your_logfile.log 2>&1
```

## Database Schema

Table: `stations`

| Column          | Type     | Description                             |
| --------------- | -------- | --------------------------------------- |
| id              | INTEGER  | Primary key                             |
| station_name    | TEXT     | Name of the station                     |
| available_bikes | INTEGER  | Number of bikes currently available     |
| empty_docks     | INTEGER  | Number of empty docks                   |
| last_updated    | DATETIME | Timestamp of last update (today's date) |

## Notes

- Script ignores duplicate entries for the same station and timestamp.
- Logs output and errors to a specified logfile when running via cron.
