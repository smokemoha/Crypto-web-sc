# Crypto Project Scraper  

## **Overview**  
This project is a **Python-based web scraper** that scans multiple cryptocurrency listing websites for **new projects that do not have websites**. It extracts information about these projects and **sends notifications to a Telegram bot**.  

The scraper collects data from:  
- **DEXTools** (`https://www.dextools.io/app/en/new-tokens`)  
- **CoinGecko** (`https://www.coingecko.com/en/coins/new`)  
- **CoinMarketCap** (`https://coinmarketcap.com/new/`)  
- **Airdrops.io** (`https://airdrops.io/latest-airdrops/`)  

## **How It Works**  
✅ Uses **Selenium** and **BeautifulSoup** to scrape websites.  
✅ Identifies **new crypto projects that have social links but no website**.  
✅ Sends real-time **notifications to a Telegram bot**.  
✅ Runs **automatically every hour** using `APScheduler`.  

---

## **Installation & Setup**  

### **Prerequisites**  
Ensure you have the following installed:  
- **Python 3.8+** → [Download Python](https://www.python.org/downloads/)  
- **Google Chrome** and **ChromeDriver**  
- **Telegram Bot Token & Chat ID** (Create a bot using [BotFather](https://t.me/BotFather) on Telegram)  

### **1️⃣ Clone the Repository**  

git clone https://github.com/YOUR-USERNAME/crypto-scraper.git
cd crypto-scraper
2️⃣ Install Dependencies

pip install requests beautifulsoup4 selenium apscheduler python-telegram-bot
3️⃣ Configure ChromeDriver
Replace the chromedriver.exe path in the script with the correct location:
python
service = Service(r'C:\path\to\chromedriver.exe')
4️⃣ Set Up Telegram Bot
Replace the following with your own Telegram bot token and chat ID:
python
TELEGRAM_TOKEN = 'your-telegram-bot-token'
CHAT_ID = 'your-chat-id'
5️⃣ Run the Scraper
python scraper.py
The scraper will start checking for new projects and send alerts to Telegram.
How It Works (Code Breakdown)
1️⃣ Web Scraping
Selenium loads dynamic content from DEXTools.
BeautifulSoup parses HTML data from CoinGecko, CoinMarketCap, and Airdrops.io.
2️⃣ Data Filtering
Collects only projects with social links but no website.
3️⃣ Telegram Notifications
Sends a message with the project name and social media links.
Example Message:
nginx
New Project: XYZ Coin
Socials: https://twitter.com/xyz, https://t.me/xyz
4️⃣ Automatic Scheduling
Runs every hour using APScheduler:
python
scheduler.add_job(main, 'interval', hours=1)
