Here's the updated, cleaner `README.md` without the extra explanations:

```md
# WebScraper

## Overview

The **WebScraper** project scrapes Craigslist for specific ticket listings, such as ACL (Austin City Limits) tickets. It filters listings based on search parameters and sends email notifications when new posts are found. The scraper uses **Selenium** for web scraping and **Gmail OAuth2** for sending email notifications.

## Features

- Scrapes Craigslist for ACL ticket listings.
- Filters listings based on criteria such as price and keywords.
- Sends email notifications for new listings.
- Automates the process using GitHub Actions to run every 15 minutes.

## Tech Stack

- **Python**: Main language for web scraping and email notifications.
- **Selenium**: Interacts with Craigslist and scrapes listings.
- **BeautifulSoup**: Parses HTML content of Craigslist pages.
- **Loguru**: Logging library for better debugging.
- **Gmail API**: Sends email notifications via OAuth2.
- **GitHub Actions**: Automates the scraping process every 15 minutes.

## Setup

### Prerequisites

1. **Python**: [Download Python](https://www.python.org/downloads/)
2. **ChromeDriver**: Download ChromeDriver and place it in `C:\WebDriver\` or update the path in the script. [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
3. **Git**: [Download Git](https://git-scm.com/)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/bradyespey/WebScaper.git
   cd WebScaper
   ```

2. **Install Dependencies**:

   Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

   Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   Create a `.env` file in the root of the project and add the following:

   ```ini
   BASE_URL=https://austin.craigslist.org/search/sss?hasPic=1&max_price=350&min_price=200&query=acl%20one%20-saturday%20-friday%20-sunday
   GMAIL_USER=your_gmail@gmail.com
   GMAIL_CLIENT_ID=your_client_id
   GMAIL_CLIENT_SECRET=your_client_secret
   GMAIL_REFRESH_TOKEN=your_refresh_token
   TOKEN_URI=https://oauth2.googleapis.com/token
   FROM_EMAIL=your_gmail@gmail.com
   TO_EMAIL=recipient_email@gmail.com
   SEEN_POSTS=src/posts.txt
   ```

4. **Run the Scraper**:

   ```bash
   python webscraper.py
   ```

   This will run the scraper and output new listings.

## Automation with GitHub Actions

This project is automated using **GitHub Actions** to run the scraper every 15 minutes and send email notifications.

### Setting Up GitHub Secrets

To securely store your Gmail credentials:

1. Go to your GitHub repository.
2. Navigate to **Settings > Secrets and variables > Actions > New repository secret**.
3. Add the following secrets:
   - `GMAIL_USER`
   - `GMAIL_CLIENT_ID`
   - `GMAIL_CLIENT_SECRET`
   - `GMAIL_REFRESH_TOKEN`
   - `TOKEN_URI`
   - `FROM_EMAIL`
   - `TO_EMAIL`

### GitHub Actions Workflow

The GitHub Actions workflow is defined in `.github/workflows/webscraper.yml`. It runs every 15 minutes, executes the scraper, and sends emails when new listings are found.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Summary of Changes:
- **Simplified instructions**: The language is now more direct, focusing solely on what the reader needs to do.
- **Removed references to previous explanations**: No mentions of "instead of" or additional clarifications that aren’t necessary for someone using the project.
- **Clear instructions**: The steps for setup, automation, and email notifications are all included in a straightforward way.

This version is streamlined and to the point. Let me know if you need anything else before pushing it to the repo!