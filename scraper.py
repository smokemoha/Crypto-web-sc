import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from telegram import Bot
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configure WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    service = Service(r'C:\Users\USER\Desktop\scarspper-web\chromedriver-win64\chromedriver.exe')  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Telegram Bot Setup
TELEGRAM_TOKEN = '7521027516:AAG4gI_Gb2-XMmde4pSpMeMewK9QGVH2IhY'  # Replace with your actual bot token
CHAT_ID = '1544638319'  # Replace with your actual chat ID
bot = Bot(token=TELEGRAM_TOKEN)

# Function to send notifications to Telegram
def send_notification(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Scrape DEXTools
def scrape_dextools():
    print("Scraping DEXTools...")
    url = "https://www.dextools.io/app/en/new-tokens"
    driver = setup_driver()
    driver.get(url)
    time.sleep(5)  # Wait for page to load (Increase this time if the page is slow to load)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    projects = []
    for project in soup.find_all('div', class_='token-list-item'):
        name = project.find('h3').text.strip()
        socials = project.find_all('a', class_='social-link')
        website = project.find('a', class_='website-link')

        # Only collect projects with social links but no website
        if socials and not website:
            social_links = [link['href'] for link in socials]
            projects.append({'name': name, 'socials': social_links})
    return projects

# Scrape CoinGecko
def scrape_coingecko():
    print("Scraping CoinGecko...")
    url = "https://www.coingecko.com/en/coins/new"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    projects = []
    for project in soup.find_all('div', class_='coin-name-wrapper'):
        name = project.find('a').text.strip()
        socials = project.find_all('a', class_='social-link')
        website = project.find('a', class_='website-link')

        if socials and not website:
            social_links = [link['href'] for link in socials]
            projects.append({'name': name, 'socials': social_links})
    return projects

# Scrape CoinMarketCap
def scrape_coinmarketcap():
    print("Scraping CoinMarketCap...")
    url = "https://coinmarketcap.com/new/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    projects = []
    for project in soup.find_all('div', class_='name-area'):
        name = project.find('p', class_='coin-item-symbol').text.strip()
        socials = project.find_all('a', class_='social-link')
        website = project.find('a', class_='website-link')

        if socials and not website:
            social_links = [link['href'] for link in socials]
            projects.append({'name': name, 'socials': social_links})
    return projects

# Scrape Airdrops.io
def scrape_airdrops():
    print("Scraping Airdrops.io...")
    url = "https://airdrops.io/latest-airdrops/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    projects = []
    for project in soup.find_all('div', class_='airdrop-item'):
        name = project.find('h3').text.strip()
        socials = project.find_all('a', class_='social-link')
        website = project.find('a', class_='website-link')

        if socials and not website:
            social_links = [link['href'] for link in socials]
            projects.append({'name': name, 'socials': social_links})
    return projects

# Combine Results
def combine_results():
    all_projects = []
    all_projects.extend(scrape_dextools())
    all_projects.extend(scrape_coingecko())
    all_projects.extend(scrape_coinmarketcap())
    all_projects.extend(scrape_airdrops())
    return all_projects

# Notify User
def notify_user(projects):
    if not projects:
        print("No new projects without websites found.")
        return

    print(f"Found {len(projects)} projects without websites:")
    for project in projects:
        print(f"Project: {project['name']}")
        print(f"Socials: {', '.join(project['socials'])}")
        print("-----")
        # Send notification to Telegram
        message = f"New Project: {project['name']}\nSocials: {', '.join(project['socials'])}"
        send_notification(message)

# Main Function
def main():
    print("Starting scraper...")
    projects = combine_results()
    notify_user(projects)

# Scheduler to Run Periodically
scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', hours=1)

if __name__ == "__main__":
    main()
