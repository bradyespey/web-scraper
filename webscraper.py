import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from loguru import logger

# Function to initialize Selenium WebDriver
def initialize_driver(headless=False):
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    
    # Path to ChromeDriver
    driver_path = r'C:\WebDriver\chromedriver.exe'  # Make sure you have the ChromeDriver here
    
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    return driver

# Function to scrape Craigslist using Selenium
def scrape_craigslist():
    driver = initialize_driver(headless=False)  # Change headless=True for headless mode

    url = 'https://austin.craigslist.org/search/sss?hasPic=1&max_price=350&min_price=200&query=acl%20one%20-saturday%20-friday%20-sunday'
    
    driver.get(url)
    
    time.sleep(5)  # Wait for page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()  # Close the browser
    
    listings = soup.find_all('li', class_='cl-search-result')
    logger.info(f"Found {len(listings)} listings.")
    
    posts = []
    for listing in listings:
        post_title = listing.find('span', class_='label').text.strip()
        post_link = listing.find('a')['href']
        post_price = listing.find('span', class_='priceinfo').text if listing.find('span', 'priceinfo') else 'N/A'
        post_location = "Austin"  # Default location for this search

        # Collect post info
        posts.append((post_title, post_location, post_link, post_price))

        # Print each post for debugging
        logger.info(f"Title: {post_title}, Price: {post_price}, Link: {post_link}")
    
    return posts

# Function to send email using Gmail API
def send_email(subject, body):
    credentials = Credentials(
        None,
        refresh_token=os.getenv('GMAIL_REFRESH_TOKEN'),
        token_uri=os.getenv('TOKEN_URI'),
        client_id=os.getenv('GMAIL_CLIENT_ID'),
        client_secret=os.getenv('GMAIL_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/gmail.send']
    )
    
    credentials.refresh(requests.Request())

    try:
        service = build('gmail', 'v1', credentials=credentials)
        message = MIMEText(body)
        message['to'] = os.getenv('TO_EMAIL')
        message['from'] = os.getenv('FROM_EMAIL')
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        sent_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        logger.info(f'Email sent successfully! Message ID: {sent_message["id"]}')
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

# Function to save scraped posts to a file
def save_to_file(posts):
    file_path = 'scraped_results.txt'  # Modify the path as needed
    with open(file_path, 'w') as f:
        for post in posts:
            f.write(f"Title: {post[0]}, Location: {post[1]}, Link: {post[2]}, Price: {post[3]}\n")
    logger.info(f"Saved {len(posts)} posts to {file_path}")

# Main function to scrape, send email, and save the results
def main():
    logger.info("Starting Craigslist scraping...")
    posts = scrape_craigslist()
    
    if posts:
        save_to_file(posts)
        
        # Prepare email body
        email_body = "\n".join([f"Title: {post[0]}, Location: {post[1]}, Price: {post[3]}, Link: {post[2]}" for post in posts])
        send_email("New Craigslist Listings", email_body)
    else:
        logger.info("No listings found.")

if __name__ == '__main__':
    main()
