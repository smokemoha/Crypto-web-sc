
import os
import requests
import logging
import time
from typing import Dict, List, Optional
from datetime import datetime
from requests.exceptions import RequestException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TelegramBot:
    def __init__(self):
       
        self.token = os.getenv('7521027516:AAG4gI_Gb2-XMmde4pSpMeMewK9QGVH2IhY')
        self.chat_id = os.getenv('1544638319')
        self.base_url = f'https://api.telegram.org/bot{self.token}'
        self.rate_limit = 30  # messages per minute
        self.last_request_time = 0
        
        if not all([self.token, self.chat_id]):
            raise ValueError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in .env file")
        
        self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('telegram_bot.log'),
                logging.StreamHandler()
            ]
        )
    
    def _rate_limit(self):
        current_time = time.time()
        time_passed = current_time - self.last_request_time
        if time_passed < (60 / self.rate_limit):
            time.sleep((60 / self.rate_limit) - time_passed)
        self.last_request_time = time.time()

    def send_message(self, message: str, retry_count: int = 3) -> Dict:
        self._rate_limit()
        
        params = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }

        for attempt in range(retry_count):
            try:
                response = requests.post(
                    f'{self.base_url}/sendMessage',
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get('ok'):
                    logging.info(f"Message sent successfully after {attempt + 1} attempts")
                    return result
                
                logging.error(f"API Error: {result.get('description')}")
                
            except RequestException as e:
                logging.error(f"Attempt {attempt + 1}/{retry_count} failed: {str(e)}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
        
        return {'ok': False, 'description': 'Max retries exceeded'}

class ProjectMonitor:
    def __init__(self, bot: TelegramBot):
        self.bot = bot
        self.processed_projects = set()
    
    def format_message(self, project: Dict) -> str:
        name = project.get('name', 'Unknown Project')
        social_links = project.get('social_links', [])
        
        return (
            f"*New Project Alert* 🚨\n"
            f"*Name:* {name}\n"
            f"*Social Links:*\n" + 
            "\n".join(f"• {link}" for link in social_links) +
            f"\n\n_Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
        )

    def check_projects(self, projects: List[Dict]) -> None:
        for project in projects:
            try:
                project_id = f"{project.get('name')}-{','.join(project.get('social_links', []))}"
                
                if (project_id not in self.processed_projects and 
                    project.get('social_links') and 
                    not project.get('website')):
                    
                    message = self.format_message(project)
                    self.bot.send_message(message)
                    self.processed_projects.add(project_id)
                    
            except Exception as e:
                logging.error(f"Error processing project {project.get('name', 'Unknown')}: {str(e)}")

def main():
    try:
        bot = TelegramBot()
        monitor = ProjectMonitor(bot)
        
        # Example projects
        projects = [
            {
                'name': 'CryptoCoin',
                'social_links': ['https://twitter.com/CryptoCoin', 'https://discord.com/CryptoCoin'],
                'website': None
            },
            {
                'name': 'TechNova',
                'social_links': ['https://twitter.com/TechNova'],
                'website': 'https://technova.com'
            }
        ]
        
        monitor.check_projects(projects)
        
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")
        raise

if __name__ == "__main__":
    main()