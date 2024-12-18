# src/youtube_scraper.py  

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

def scrape_youtube_video(video_url):
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
        time.sleep(5)  # Initial load
        
        # Wait for title to be present
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ytd-video-primary-info-renderer"))
        ).text.strip()
        
        # Get view count
        views = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.ytd-video-view-count-renderer"))
        ).text.strip()
        
        # Get likes
        likes = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-menu-renderer span.ytd-toggle-button-renderer"))
        ).text.strip()

        video_data = {
            "Title": title,
            "Views": views,
            "Likes": likes
        }

        # Save to CSV
        df = pd.DataFrame([video_data])
        df.to_csv('data/videos.csv', mode='a', index=False, header=False)

        print("Video data scraped and saved.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()