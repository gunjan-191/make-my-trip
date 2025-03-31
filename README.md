# MakeMyTrip Hotel Scraper

This Python script scrapes hotel data from MakeMyTrip, collects hotel URLs, and stores the collected data in a MongoDB database. It uses Selenium with Undetected ChromeDriver to handle dynamic content loading.

## Features
- Scrapes hotel URLs from a search results page.
- Captures and stores cookies and headers for authenticated requests.
- Saves hotel data directly to MongoDB.
- Scrolls through dynamically loaded content for better data coverage.

## Requirements
- Python 3.x
- Selenium
- undetected-chromedriver
- pymongo
- requests
- Chrome Browser

## Installation
```bash
pip install selenium undetected-chromedriver pymongo requests
```

## MongoDB Setup
1. Create a MongoDB database.
2. Replace the `CONNECTION_STRING` with your credentials:

```python
CONNECTION_STRING = "mongodb+srv://<db_username>:<db_password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
```

## Usage
1. Update your `db_username` and `db_password` variables.
2. Run the script using:
```bash
python your_script_name.py
```

## Code Explanation
### 1. Initialization
- Sets up a connection to MongoDB.
- Opens the MakeMyTrip search page via Selenium and undetected ChromeDriver.

### 2. Collecting Hotel URLs
- Scrolls through the hotel listing page until all content is loaded.
- Extracts URLs of the first 10 hotels.

### 3. Saving Data to MongoDB
- Uses `pymongo` to save hotel data in the `HotelDatabase` collection.

### 4. Extracting Headers and Cookies
- Opens each hotel URL to capture valid headers and cookies.
- Uses these headers and cookies to make authenticated requests to MakeMyTrip.

## Potential Improvements
- Error handling for network failures or invalid cookies.
- Automating the cookie and header extraction process.
- Increasing the number of hotels scraped.
- Adding support for multiple pages.

## License
This project is licensed under the MIT License.

