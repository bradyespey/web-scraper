import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64

# Load environment variables from .env file
load_dotenv()

# Gmail credentials from environment variables
GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
GMAIL_REFRESH_TOKEN = os.getenv('GMAIL_REFRESH_TOKEN')
TOKEN_URI = os.getenv('TOKEN_URI')
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')

# Function to initialize Selenium WebDriver
def initialize_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    driver_path = r'C:\WebDriver\chromedriver.exe'
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to scrape listings using Selenium
def scrape_craigslist():
    driver = initialize_driver(headless=False)
    url = 'https://austin.craigslist.org/search/sss?hasPic=1&max_price=350&min_price=200&query=acl%20one%20-saturday%20-friday%20-sunday'
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    listings = soup.find_all('li', class_='cl-search-result')
    logger.info(f"Found {len(listings)} listings.")
    posts = []
    for listing in listings:
        post_title = listing.find('span', class_='label').text.strip()
        post_link = listing.find('a')['href']
        post_price = listing.find('span', class_='priceinfo').text if listing.find('span', 'priceinfo') else 'N/A'
        post_location = "Austin"
        posts.append((post_title, post_location, post_link, post_price))
        logger.info(f"Title: {post_title}, Price: {post_price}, Link: {post_link}")
    return posts

# Function to send email via Gmail API
def send_email(subject, body):
    credentials = Credentials(
        None,
        refresh_token=GMAIL_REFRESH_TOKEN,
        token_uri=TOKEN_URI,
        client_id=GMAIL_CLIENT_ID,
        client_secret=GMAIL_CLIENT_SECRET,
        scopes=['https://mail.google.com/']
    )
    try:
        logger.info("Refreshing token...")
        logger.info(f"Credentials before refresh: Valid: {credentials.valid}, Scopes: {credentials.scopes}")
        
        # Try to refresh the token
        credentials.refresh(Request())

        logger.info(f"Credentials after refresh: Valid: {credentials.valid}")
        
        # Send email via Gmail API
        service = build('gmail', 'v1', credentials=credentials)
        message = MIMEText(body)
        message['to'] = TO_EMAIL
        message['from'] = FROM_EMAIL
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Add more logging around the email sending process
        logger.info("Sending email...")
        sent_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()

        # Print the entire `sent_message` response to see what it contains
        logger.info(f'Email sent successfully! Response: {sent_message}')
        if isinstance(sent_message, dict) and 'id' in sent_message:
            logger.info(f'Email Message ID: {sent_message["id"]}')
        else:
            logger.error(f"Unexpected response format: {sent_message}")

    except Exception as e:
        logger.error(f"Error during token refresh or email send: {e}")
        logger.error(f"Error details: {str(e)}")
        logger.error(f"Credentials Object: {credentials}")

# Function to save the scraped posts to a file
def save_to_file(posts):
    file_path = os.path.join(os.path.dirname(__file__), 'scraped_results.txt')
    with open(file_path, 'w') as f:
        for post in posts:
            f.write(f"Title: {post[0]}, Location: {post[1]}, Link: {post[2]}, Price: {post[3]}\n")
    logger.info(f"Saved {len(posts)} posts to {file_path}")

# Main function to orchestrate the scraping process
def main():
    logger.info("Starting Craigslist scraping...")
    posts = scrape_craigslist()
    if posts:
        email_body = "\n".join([f"Title: {post[0]}, Location: {post[1]}, Price: {post[3]}, Link: {post[2]}" for post in posts])
        send_email("New Craigslist Listings", email_body)
        save_to_file(posts)
    else:
        logger.info("No listings found.")

if __name__ == '__main__':
    main()
