import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
def getData():
    """Fetch data from all 4 station combinations using Selenium"""
    all_rows = []
    coordinates = ["00", "01", "10", "11"]
    
    # Setup Chrome driver with headless option and anti-detection measures
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # Use new headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Additional preferences to avoid detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    
    # Execute script to remove webdriver property
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        for coord in coordinates:
            x = coord[0]
            y = coord[1]
            url = f"https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:{x}/Y:{y}/station:0"
            
            print(f"Fetching data for X:{x}, Y:{y}...")
            driver.get(url)
            
            # Wait for page to load and get the pre tag content
            time.sleep(2)  # Give it time to load
            page_source = driver.page_source
            
            # Extract JSON from page
            try:
                # Find the body text which contains the JSON
                body = driver.find_element(By.TAG_NAME, "body")
                json_text = body.text
                data = json.loads(json_text)
                
                if "data" in data and "rows" in data["data"]:
                    rows = data["data"]["rows"]
                    all_rows.extend(rows)
                    print(f"Loaded {len(rows)} records from X:{x}, Y:{y}")
                else:
                    print(f"Warning: No rows found for X:{x}, Y:{y}")
            except Exception as e:
                print(f"Error parsing JSON for X:{x}, Y:{y}: {e}")
    
    finally:
        driver.quit()
    
    return all_rows

def convertData(all_rows):
    """Convert rows to CSV with timestamp filename"""
    if all_rows:
        df = pd.DataFrame(all_rows)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{timestamp}.csv"
        df.to_csv(output_file, index=False)
        print(f"Converted {len(all_rows)} total records to {output_file}")
    else:
        print("No data found")

if __name__ == "__main__":
    all_rows = getData()
    convertData(all_rows)