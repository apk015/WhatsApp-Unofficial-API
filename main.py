import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
from time import sleep
from rich.progress import Progress, BarColumn, TimeRemainingColumn
import logging
from dotenv import load_dotenv
import argparse
import signal

# Load environment variables
load_dotenv()

# Setup logging
LOG_FILE = os.getenv("LOG_FILE", "whatsapp_unofficial_api.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppBot:
    def __init__(self, delay=30):
        self.delay = delay
        self.driver = self.init_driver()
        self.progress = self.load_progress()
        self.log = self.load_log()
        self.message_template = self.load_message_template()

    @staticmethod
    def init_driver():
        """ Initialize Chrome driver with options """
        CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
        USER_DATA_DIR = os.getenv('USER_DATA_DIR')

        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        options.add_argument("--profile-directory=Default")

        service = ChromeService(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://web.whatsapp.com')
        return driver

    @staticmethod
    def load_data(file_path=os.getenv("CONTACTS_CSV", 'contacts.csv')):
        """ Load and format contacts CSV """
        try:
            df = pd.read_csv(file_path).astype(str)
            df.drop_duplicates(subset='phone', inplace=True)
            return df
        except Exception as e:
            logging.error(f"Error loading contacts CSV: {e}")
            return pd.DataFrame()

    @staticmethod
    def load_log(file_path='log.json'):
        """ Load or create log file """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logging.warning("Log file corrupted. Recreating.")
        return {"successful": [], "failed": [], "duplicates": []}

    @staticmethod
    def save_log(log, file_path='log.json'):
        """ Save log to file """
        with open(file_path, 'w') as file:
            json.dump(log, file, indent=4)

    @staticmethod
    def load_progress(file_path='progress.json'):
        """ Load or create progress tracking file """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logging.warning("Progress file corrupted. Starting fresh.")
        return {"last_processed": -1}

    @staticmethod
    def save_progress(progress, file_path='progress.json'):
        """ Save progress to file """
        with open(file_path, 'w') as file:
            json.dump(progress, file, indent=4)

    @staticmethod
    def load_message_template(file_path='msg.txt'):
        """ Load message template from file """
        try:
            with open(file_path, 'r', encoding="utf8") as f:
                return f.read().strip()
        except FileNotFoundError:
            logging.error("Message template file not found.")
            return ""

    @staticmethod
    def format_phone_number(phone):
        """ Format phone numbers by stripping non-digits and leading zeros """
        phone = ''.join(filter(str.isdigit, phone))
        return phone[1:] if phone.startswith('0') else phone

    def send_message(self, contact, message, image_path=None):
        """ Send a message (and optionally an image) via WhatsApp """
        try:
            # Navigate to WhatsApp Web with message
            self.driver.get(f'https://web.whatsapp.com/send?phone={contact}&text={quote(message)}')

            # Wait for message box to load
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            sleep(2)  # Allow the page to stabilize

            if image_path and os.path.exists(image_path):
                logging.info(f"Attaching image for {contact}")
                self.attach_image(image_path)
                # Handle clicking the "Send" button after image is attached (popup mode)
                self.click_send_button_after_image()
            else:
                # Handle clicking the "Send" button for text-only messages
                self.click_send_button()

            logging.info(f"Message sent successfully to {contact}")
            return True

        except Exception as e:
            logging.error(f"Failed to send message to {contact}: {e}")
            return False

    def attach_image(self, image_path):
        """ Handle attaching an image to the message """
        try:
            attachment_button = WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Attach"]'))
            )
            attachment_button.click()

            image_input = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
            )
            image_input.send_keys(image_path)

            WebDriverWait(self.driver, self.delay).until(
                EC.visibility_of_element_located((By.XPATH, '//img[@alt="Preview"]'))
            )
            sleep(2)  # Let the preview stabilize

        except Exception as e:
            logging.error(f"Failed to attach image: {e}")

    def click_send_button(self):
        """ Handle clicking the "Send" button for text-only messages """
        try:
            send_button = WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
            )
            send_button.click()
            sleep(3)

        except Exception as e:
            logging.error(f"Send button click failed: {e}")

    def click_send_button_after_image(self):
        """ Handle clicking the correct "Send" button after an image is attached """
        try:
            send_button = WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Send"]'))
            )
            send_button.click()
            sleep(3)

        except Exception as e:
            logging.error(f"Send button click after image failed: {e}")

    def process_contacts(self, batch_size):
        """ Process contacts in batches and send messages """
        df = self.load_data()
        total_contacts = len(df)

        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            "[progress.completed]{task.completed}/{task.total}",
            TimeRemainingColumn(),
        ) as progress_bar:
            task = progress_bar.add_task("Sending Messages", total=batch_size)

            for i in range(self.progress["last_processed"] + 1, total_contacts):
                if i >= batch_size:
                    break

                row = df.iloc[i]
                contact = self.format_phone_number(row['phone'])
                message = self.message_template.format(**row.to_dict())

                if contact in self.log["successful"] or contact in self.log["failed"]:
                    self.log["duplicates"].append(contact)
                    progress_bar.advance(task)
                    continue

                success = self.send_message(contact, message)
                if success:
                    self.log["successful"].append(contact)
                else:
                    self.log["failed"].append(contact)

                # Update progress
                self.progress["last_processed"] = i
                self.save_progress(self.progress)
                self.save_log(self.log)
                progress_bar.advance(task)

        logging.info("Batch processing completed.")

    def run(self, batch_size):
        """ Start the process """
        input("Sign in to WhatsApp Web and press ENTER...")
        self.process_contacts(batch_size)
        self.driver.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="WhatsApp Unofficial API")
    parser.add_argument('--batch-size', type=int, default=10, help="Number of contacts to process in each batch")
    parser.add_argument('--image', type=str, default=None, help="Optional image path to send with messages")
    return parser.parse_args()

def handle_exit(signum, frame):
    print("Gracefully shutting down...")
    bot.save_progress(bot.progress)
    bot.save_log(bot.log)
    bot.driver.quit()
    exit(0)

if __name__ == "__main__":
    args = parse_args()
    bot = WhatsAppBot()

    # Handle graceful shutdown on CTRL+C
    signal.signal(signal.SIGINT, handle_exit)

    bot.run(args.batch_size)
