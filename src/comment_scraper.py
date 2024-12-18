# src/comment_scraper.py  

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

def scrape_youtube_comments(video_url):
    # Get Bright Data credentials
    CUSTOMER_ID = os.getenv('BRIGHT_DATA_CUSTOMER_ID')
    ZONE_NAME = os.getenv('BRIGHT_DATA_ZONE_NAME')
    
    # Configure Chrome options for Bright Data
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Add Bright Data proxy
    proxy = f'http://brd-customer-{CUSTOMER_ID}-zone-{ZONE_NAME}:[email protected]:22225'
    chrome_options.add_argument(f'--proxy-server={proxy}')
    
    try:
        print('Initializing Chrome WebDriver...')
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        print(f'Connected! Navigating to {video_url}...')
        driver.get(video_url)
        time.sleep(5)  # Wait for initial load
        
        # Scroll down to load more comments
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)

        comments = driver.find_elements(By.CSS_SELECTOR, 'yt-formatted-string#content-text')
        all_comments = [comment.text for comment in comments]
        
        # Save to CSV
        df = pd.DataFrame(all_comments, columns=["Comment"])
        df.to_csv('data/comments.csv', index=False)

        print("Comments scraped and saved.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()