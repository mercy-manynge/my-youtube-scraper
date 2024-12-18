# src/main.py  

import os
from youtube_scraper import scrape_youtube_video  
from comment_scraper import scrape_youtube_comments  

def ensure_data_directory():
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Create videos.csv with headers if it doesn't exist
    if not os.path.exists('data/videos.csv'):
        with open('data/videos.csv', 'w') as f:
            f.write('Title,Views,Likes\n')
    
    # Create comments.csv with headers if it doesn't exist
    if not os.path.exists('data/comments.csv'):
        with open('data/comments.csv', 'w') as f:
            f.write('Comment\n')

def main():  
    video_url = "https://www.youtube.com/watch?v=SqcY0GlETPk"  # Replace with your target URL  

    # Ensure data directory and files exist
    ensure_data_directory()

    # Scrape video details  
    scrape_youtube_video(video_url)  

    # Scrape comments  
    scrape_youtube_comments(video_url)  

if __name__ == "__main__":  
    main()