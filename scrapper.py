import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, json,requests
from pymongo import MongoClient

####add your password and username
db_password= ""
db_username=""
CONNECTION_STRING = "mongodb+srv://<db_username>:<db_password>@cluster0.jvbssi1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

#####Initialize the client
client = MongoClient(CONNECTION_STRING)

# Connect to your database and collection
db = client["HotelDatabase"]
collection = db["HotelResponses"]

# URL to scrape
url = "https://www.makemytrip.com/hotels/hotel-listing/?checkin=04052025&checkout=04092025&locusId=CTPNQ&locusType=city&city=CTPNQ&country=IN&searchText=Viman%20Nagar&roomStayQualifier=1e0e&_uCurrency=INR&mmAreaTag=Viman%20Nagar%7CARVIM&reference=hotel&type=city&rsc=1e1e0e"

# Setting up Undetected ChromeDriver
driver = uc.Chrome()
driver.get(url)
time.sleep(5)  # Allow the page to load

# Scroll down to load hotels
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Exit loop if no new content is loaded
    last_height = new_height

# Collecting hotel URLs
hotel_urls = []
hotel_blocks = driver.find_elements(By.XPATH, '//div[contains(@class,"listingRowOuter hotelTileDt")]')

# Loop through the first 10 hotel blocks (or fewer if less than 10 available)
for i, hotel_block in enumerate(hotel_blocks[:10]):
    try:
        a_href = hotel_block.find_element(By.XPATH, './/a').get_attribute("href")
        hotel_urls.append(a_href)
        print(f"Hotel {i+1} URL collected: {a_href}")
    except Exception as e:
        print(f"Error collecting URL for hotel {i+1}: {e}")


def save_to_mongo(data, collection):
    if isinstance(data, dict):  # If it's a single record (dictionary)
        collection.insert_one(data)
    elif isinstance(data, list):  # If it's multiple records (list of dictionaries)
        collection.insert_many(data)
    print("Data saved to MongoDB successfully!")

def get_valid_headers_and_cookies(url: str, driver, id_):
  
    driver.get(url)
    time.sleep(15)  # Wait for the page to load completely
    checkin = driver.find_element(By.XPATH, '//label[@for="checkin"]')
    driver.execute_script("arguments[0].click();", checkin)
    time.sleep(10)

  
    # Get cookies
    cookies = driver.get_cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    # Get headers
    headers = {
      'accept': 'application/json',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'content-type': 'application/json',
      'currency': 'INR',
      'entity-name': 'india',
      'language': 'eng',
      'origin': 'https://www.makemytrip.com',
      'os': 'desktop',
      'priority': 'u=1, i',
      'referer': 'https://www.makemytrip.com/',
      'region': 'IN',
      'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'server': 'b2c',
      'tid': 'avc',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
      'user-country': 'IN',
      'user-currency': 'INR',
      'usr-mcid': '23160196828617794324591280495500123035',
      'vid': '4c5276ef-b8f1-420e-81c3-f34cfeeb4c12',
      'visitor-id': '4c5276ef-b8f1-420e-81c3-f34cfeeb4c12',
      # 'Cookie': 'isGdprRegion=0; lang=eng; ccde=IN; GL=true; isWW=0; userCurrency=INR; dvid=27f75ed9-1ddc-482d-9b0f-beaedf192745; bm_ss=ab8e18ef4e; bm_so=D39FBBE52AF474F6FE77F6AB537A8038621A1E6D481C6A8670EB7C11B3640DE9~YAAQVW4/FzK5+KyVAQAAP73o6gMOid7V3t95H1nmfqCjCTjyfh26g5UNw8Rk1RfCmo3sWrpQ1LqfejtGmzeMyzIBprKEwrniQWF0vck6STeLcaHKk/xTj8SXv7Ykt5Lk1Se+dcMwWqlJZoh6d7KbgG+laFFen5xW8SoI9mwmVsJ8QPJfrr/uNQfTt5p4S/QKkQjWgsOr3pQuyRaVC9+4MiFoZ7JM6mRfy36vpR2hfDECWByM4SQDniAjrr1OOR/6k3fRSS3Q3W9d0uMu7QUCa0Sa7WM4pTxCirEoLOxYc8qFejX1kXhvKpDupvi3zE7zP0p8mFCbXV6tKNnSbYCsaVisn+RwRDTSpg/3j+8sPKP3zk0w9Q0dKprKRlEGRpVXnGVoPslDkTHZtILYVFXoaIqKtufyOFSmcAVY5xsxgTSLLToMU4vH42h0NuJ494HpfNsYl2Rjc2UoSGZgINLAlPnRAdI=; mcid=4c5276ef-b8f1-420e-81c3-f34cfeeb4c12; AMCVS_1E0D22CE527845790A490D4D%40AdobeOrg=1; s_ecid=MCMID%7C23160196828617794324591280495500123035; AMCV_1E0D22CE527845790A490D4D%40AdobeOrg=-1712354808%7CMCIDTS%7C20179%7CMCMID%7C23160196828617794324591280495500123035%7CMCAAMLH-1744007677%7C12%7CMCAAMB-1744007677%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1743410077s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; ak_bmsc=A2DBFD49D959B19CB4CB8AE87272BAA7~000000000000000000000000000000~YAAQVW4/F5O5+KyVAQAAgcTo6hs11bWu+iPCQiNzhRF8CCtI37fe/87I/KbzfCQYgnlXMJIeqwu63jOMDr6DHCTvmVVQaqq1wdG510Hfr2c5jU9TAUFf2FWTxKkmengo4XGurBcy3hAyg0sz13j+bpv6MlLQyoZIPDLF6J1VpFShc15dT/xId1RVJogLxrv6KX4zP70cG2bcNAvTWOGvudNDd+ttoq01kHZozhL9VsQnfd4BIEmK3RFyf7CkvPUuN/IGyOlA22Zwzx3e6nByG/lopm0YdTwaJctAF25pgHOScX0erCKg6sD6ZppKPbsfy12ebiNbflnkCnBtYZMRl/4HkhjoLsHwtVw0h9vlrKVhEgYMuIcv3BHkUXMDJeqS8eZaKxhlzb4byZfqGC7PZ25A/ba9JegoW1gbouQtU/M+zbZMgaa9CGLx+R7ER8zPneaNPhAYNoIEivbEtwW411u5; _gcl_au=1.1.594871319.1743402883; _fbp=fb.1.1743402883421.22370474736973512; MMYTUUID=24617072-3124-747a-3053-39425730242f.1743402883204849; RSDT=1; s_pers=%20s_depth%3D1%7C1743404678434%3B%20s_vnum%3D1743445800438%2526vn%253D1%7C1743445800438%3B%20s_lv%3D1743402888281%7C1838010888281%3B%20s_lv_s%3DFirst%2520Visit%7C1743404688281%3B%20gpv_pn%3Dfunnel%253Adomestic%2520hotels%253Ahoteldetails%7C1743404688282%3B%20s_invisit%3Dtrue%7C1743404688282%3B%20s_nr3650%3D1743402888283-New%7C2058762888283%3B%20s_nr30%3D1743402888283-New%7C1745994888283%3B%20s_nr120%3D1743402888283-New%7C1753770888283%3B%20s_nr7%3D1743402888284-New%7C1744007688284%3B; s_sess=%20s_cc%3Dtrue%3B%20tp%3D13941%3B%20s_ppv%3Dfunnel%25253Adomestic%252520hotels%25253Ahoteldetails%252C4%252C4%252C585%3B%20s_sq%3D%3B; bm_sz=E8A7F3557D33F24FBE9E481C0EF52BC0~YAAQVW4/FzG8+KyVAQAAdu/o6hviiHkePcR8V8+u9HfGYPJUjhGMAVNsKzk5+4qckfSTNZwcKTZCrcvZX88bPWnrHdZ2lwbZzgkmSpYjtF0A6VMu/IPA/bGMbsT68FPuUniJMHAXLPMyYSjPQowgEg/i0uYQr/B5JOKVYtDoWj4nmLEgs5KcDp3c129NktrWdqBdvzfCHNwc36jTw7PyGgU1zdXDE1lNbuTZNo2cnj1SgHcZxT3XeY6EoMranOr1rvw2vB6bQ5PxpeRV+AHqrTZeYbRtv7GxreLF0Pp6FxLHtG1qh4kojSlCumqczFdoyYgtAbVfwVwpOXweAZy+l1IRISNHyKLa13digsdK3ndr3S6jym3tMnQ7/JrPAn9Q2mNqskGxyKfhgYtIq3YGOSfVihhSkQmQw0v8K4LkeMU=~4404016~3420720; _abck=FC79D2096F3351C4A7481106F7D58092~0~YAAQVW4/FzK8+KyVAQAAuu/o6g2cB0AfxR9gmjfIsMIYU1O240DrQOtS4cm8KKB9mbivAX6OHn3gZcRMOua0ABa18X12s2fHguUF5UzvGHydMt1i2nxPV4hEM/1UJJByt+inLhEb4xZx2SV/43Y8htNA0JZJXEuvwYorET3i6tkw5+ONUaHl9bjhMk4kxFcxMetNqLH/MGNj+1s5W/06HEjfAajd5LdjYBb4ZBsE54wurS/758ZxIPGk0YVPUKVdhkuwc/WqXlwDeC+pdaook2SKICdoeAxGjxLztQcJ/woiAr8zr8rShnYk3KNe8j5DKF2xJ2/ua21IG5Wg+SN0cCQhzWOItGppkEfmF6escDkKgS6pORGT5eSzO/Nx0ZcfN/9/+VnV+h/toC+Sum96nTUkOFRGA188kn4ACapifRd6JcePg9cebI5JbAW8iLDrzCYV38p/8MNUkgqUyGpiifEKyzJjIMt2O0hIf1WFYyJBXsjU9iX/fznCbY2cEaxGln1mQ/s/QDVJP48KBn/PBHq+rU+f5QvgpDFTq8sV4G8=~-1~-1~-1; bm_s=YAAQVW4/F0C8+KyVAQAAm/Ho6gPZLnbVyCUh/1CkGH9VNUFyFvz4RY9vKE/g9DJmrCQz5bYJ2ZCjykzH57UDut52kH4J3De4rMFJyoAIkG4bHceUGCD8jibLQhM3mMjhZXUqMiOa0AhiGvR/o9bWjJ1n3kRNimwb8fhtDeXiCkI1Nfno1bkzhS6SP5ls9wEbRhJVV+re7hhQ1XjjsJd31wR+pGHr30JG17v/qyG9HT89MYVHStFv9/fDOMBcDCihVnN68NJvdERA6Eroqp1dNGLXSKTrSuZM/Sd4RcFhU9C5wbpEPjnHS1UhZtALpGnhEcsqc3hilCs9fuLmd4QyacGPJcxH44Yh/AMuH+50eto+9tH1Iz8wiN5a99Tn16anuPgnM9ci41J3KcBAowDrqwMl7XC37zD/e7z44jM3GoxdnvWeDltzJoP6sWUsY1GUXQbH56q9LOnssHYF4XXA; visitNumber=%7B%22number%22%3A1%2C%22time%22%3A1743402889789%7D; MMYTUUID=24617072-3124-4951-6249-37546f62244f.1743405160747094; _abck=FC79D2096F3351C4A7481106F7D58092~-1~YAAQkc5JF/uretWVAQAAK58L6w0rOGNCQzpSQk2AEjuZSyJ39R0lXddY6FYewVcY4C0XO1LlX9e9VmSujRlZ+SP7CQvfC5+88425brqlU850BrX9O4Uiyp6O5pVmb8LJ/4X9Yb8TNtJFeX9fFWiFXDuXKqX+LxBwdmqTBzbjFUAL4y0u2qtXzf7iVKtyCU6pO5f6x60p7DhsLsg3v49AXgC0vFcK2yUDSQG86gZpBZHKaPVaSob71M3OWMQ9q0b0DJibpdUIsI9ZFjb7Hy32dDzmP7MwDumQIW273Jqd6X4/yGRKvB8VsazuBcz7Y++NeUa4ujaNeAq6O+xkNEs43LhV2QESNngm9++ANDXq2t4VQR74HI7mixgoEEfTMc+8xF4JXpaXVwqkzMklIzxbV4/u0KQY+Q/u7Ip4AIhoxo4GXs1jNfmbc/sYdFJfXDHpy5YQbmk7lqEI0zJBWH4Wykok07nm7NCmZUDqxFhGgwTfADcQqf4vrIgYhdpM0zf4RlOOoxkCS1m+ZF9XImxX7Y8TlNOdzfXTpjPwzDl5P1A=~0~-1~-1; bm_s=YAAQmM5JF0+0FtmVAQAAP3RX5QNG+MIH0CbpOze267TwM6P6po+rnB2FUNCHulxpKsCyjsii8dYaz+qupk8tiQHwpyDYBJTsuNBvBnV3p72wAbMv5yi0MrA1MIjmT3qOFO/zk3Zjs70BprQEI7CC5y8v74mQQqP05mUAwFMUqws54nLYSSIhECRDXlC4dox9C6dnD+QobE/0XP06aBFW9tdAFawTbapRD1zbilNxQ53f2+L92jiBZku+ekgmfw1V0vIpRJQx8YyY6NQJsqV//sVJXLFGPvz0Y3I/KZMLqJ+QntvIgLhVA2tAdpVpQB5iI0B0Ip0AaO4FDq1SrCJHqDrw0Jg5aVdn5qdsoh8M1Ad8vhsuwR8AH1J+VhWDFIlxeT7lyO0ibpIXfFese9WuL3FVbDcnhZ389eTwk3a9WRB9dTXtvDsmayqsXPyuLZUsppXyn2RorqQAi6Ckq7fB'
    }

    payload = json.dumps({
        "deviceDetails": {
          "appVersion": "134.0.0.0",
          "deviceId": "27f75ed9-1ddc-482d-9b0f-beaedf192745",
          "deviceType": "Desktop",
          "bookingDevice": "DESKTOP",
          "deviceName": None
        },
        "searchCriteria": {
          "hotelId": id_,#"202205162302075206",
          "checkIn": "2025-04-01",
          "checkOut": "2025-04-04",
          "roomStayCandidates": [
            {
              "adultCount": 1,
              "rooms": 1,
              "childAges": []
            }
          ],
          "comparatorHotelIds": [],
          "countryCode": "IN",
          "cityCode": "CTPNQ",
          "locationId": "CTPNQ",
          "locationType": "city",
          "currency": "INR",
          "limit": 20,
          "personalCorpBooking": False,
          "userSearchType": "hotel"
        },
        "requestDetails": {
          "visitorId": "4c5276ef-b8f1-420e-81c3-f34cfeeb4c12",
          "visitNumber": 1,
          "journeyId": "71265882627f75ed9-1ddc-482d-9b0f-beaedf192745",
          "requestId": "25c2d89e-f299-46be-b494-e18dace3ff40",
          "sessionId": "d0b14df6-fd78-4dda-8371-90aa0a8396cb",
          "trafficSource": None,
          "loggedIn": False,
          "couponCount": 3,
          "funnelSource": "HOTELS",
          "idContext": "B2C",
          "notifCoupon": None,
          "pageContext": "DETAIL",
          "channel": "B2Cweb",
          "seoCorp": False,
          "payMode": None,
          "isExtendedPackageCall": False,
          "forwardBookingFlow": False
        },
        "featureFlags": {
          "addOnRequired": True,
          "applyAbsorption": True,
          "bestCoupon": True,
          "freeCancellationAvail": True,
          "responseFilterFlags": True,
          "soldOutInfoReq": True,
          "walletRequired": True,
          "bestOffersLimit": 3
        },
        "filterCriteria": [],
        "expData": "{APE:10,PAH:5,PAH5:T,WPAH:F,BNPL:T,MRS:T,PDO:PN,MCUR:T,ADDON:T,CHPC:T,AARI:T,NLP:Y,RCPN:T,PLRS:T,MMRVER:V3,BLACK:T,IAO:F,BNPL0:T,EMIDT:1,GBE:T,CV2:T,MLOS:T,SOU:T,APT:T,SRRP:T,AIP:T,PLV2:T,RTBC:T,SPKG:T,TFT:T,GALLERYV2:T,NDD:T,UGCV2:T}",
        "userLocation": {
          "city": "CTFARI",
          "state": "STHR",
          "country": "IN"
        }
      })


    return headers, cookie_dict , payload


def make_request(url: str, headers: dict, cookies: dict, payload :dict):
    # new_request_id = str(uuid.uuid4())
    new_request_id = "c7761196-065d-4c6e-97bf-6ba013c409d4"
    print("qabc")
    time.sleep(30)
    print(":::")
    url = f"https://mapi.makemytrip.com/clientbackend/cg/search-rooms/DESKTOP/2?language=eng&region=in&currency=INR&idContext=B2C&countryCode=IN&requestId={new_request_id}"
    response = requests.post(url, headers=headers, cookies=cookies, data=payload)
    

    # Attempt to parse JSON if the response is valid
    try:
        json_data = response.json()
        print("Parsed JSON Response:", json.dumps(json_data, indent=4))
    except json.JSONDecodeError:
        print("Response is not in JSON format.")
    
    return response.text


# ####Visit each hotel URL and extract data
for index, hotel_url in enumerate(hotel_urls, start=1):
    hotel_id = hotel_url.split("hotelId=")[1].split("&")[0]
    print(hotel_url , hotel_id)

    target_url = f"https://www.makemytrip.com/hotels/hotel-details/?checkin=04012025&checkout=04042025&locusId=CTPNQ&locusType=city&city=CTPNQ&country=IN&searchText=Viman%20Nagar&roomStayQualifier=1e0e&_uCurrency=INR&mmAreaTag=Viman%20Nagar%7CARVIM&reference=hotel&hotelId={hotel_id}&rf=directSearch&type=hotel&rsc=1e1e0e&viewType=BUDGET"

    time.sleep(5)

      
    headers, cookies, payload = get_valid_headers_and_cookies(target_url, driver,hotel_id)

      
    print("Headers:", json.dumps(headers, indent=4))

    time.sleep(120)

    response_data = make_request(target_url, headers, cookies, payload)

    print("Response Data:", json.dumps(response_data, indent=4))

    save_to_mongo(response_data, collection)




    

    



    


