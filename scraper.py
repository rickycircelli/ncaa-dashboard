import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Scrapes TFRRS meet results from a given athlete profile URL
def scrape_tfrrs_results(url, wait_time=15):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(wait_time)  # Wait for JS to load; you can adjust wait_time if needed

        tables = driver.find_elements(By.TAG_NAME, 'table')
        data = []

        for table_index in range(4, len(tables)):
            table = tables[table_index]
            text = table.text.strip().split('\n')
            if len(text) >= 2:
                meet_info = text[0]
                for line in text[1:]:
                    parts = line.split()
                    if len(parts) >= 2:
                        event = parts[0]
                        mark = parts[1]
                        place = ' '.join(parts[2:]) if len(parts) > 2 else ''
                        data.append([meet_info, event, mark, place])

        df = pd.DataFrame(data, columns=['Meet_Info', 'Event', 'Mark', 'Place'])
        return df

    finally:
        driver.quit()
