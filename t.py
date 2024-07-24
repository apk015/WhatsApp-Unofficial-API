import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from time import sleep
from rich.progress import Progress, BarColumn, TimeRemainingColumn

# Set up Chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

# Function to load and process CSV file
def load_data():
    df = pd.read_csv('contacts.csv')  # Use the correct path for the CSV file
    df = df.astype(str)  # Convert all columns to string
    df.drop_duplicates(subset='phone', inplace=True)
    return df

# Function to load log file
def load_log():
    if os.path.exists('log.json'):
        try:
            with open('log.json', 'r') as file:
                log = json.load(file)
        except json.JSONDecodeError:
            print("Log file is corrupted. Recreating the log file.")
            log = {"successful": [], "failed": [], "duplicates": []}
            save_log(log)
    else:
        log = {"successful": [], "failed": [], "duplicates": []}
    return log

# Function to save log file
def save_log(log):
    with open('log.json', 'w') as file:
        json.dump(log, file, indent=4)

# Function to save progress file
def save_progress(progress):
    with open('progress.json', 'w') as file:
        json.dump(progress, file, indent=4)

# Function to load progress file
def load_progress():
    if os.path.exists('progress.json'):
        try:
            with open('progress.json', 'r') as file:
                progress = json.load(file)
        except json.JSONDecodeError:
            print("Progress file is corrupted. Starting from the beginning.")
            progress = {"last_processed": -1}
    else:
        progress = {"last_processed": -1}
    return progress

# Function to format phone number
def format_phone_number(phone):
    phone = ''.join(filter(str.isdigit, phone))  # Remove all non-digit characters
    if phone.startswith('0'):
        phone = phone[1:]  # Remove leading zero if present
    return phone

# Function to send WhatsApp message
def send_message(contact, message):
    try:
        driver.get(f'https://web.whatsapp.com/send?phone={contact}&text={quote(message)}')
        send_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )
        sleep(1)
        send_button.click()
        sleep(3)
        return True
    except Exception as e:
        return False

# Main function
def main(batch_size):
    # Load data and logs
    df = load_data()
    log = load_log()
    
    # Ensure all necessary keys are present in the log
    for key in ["successful", "failed", "duplicates"]:
        if key not in log:
            log[key] = []

    progress = load_progress()

    # Read message template from file
    with open("msg.txt", "r", encoding="utf8") as f:
        message_template = f.read().strip()

    # Progress bar setup using rich
    total = len(df)
    start_index = progress["last_processed"] + 1
    end_index = min(start_index + batch_size, total)

    successful_count = 0
    failed_count = 0
    duplicate_count = 0

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        "[progress.completed]{task.completed}/{task.total}",
        "•",
        "Successful: {task.fields[successful]} Failed: {task.fields[failed]} Duplicates: {task.fields[duplicates]}",
        "•",
        TimeRemainingColumn(),
    ) as progress_bar:
        task = progress_bar.add_task("Sending Messages", total=end_index - start_index, start=0, 
                                     successful=successful_count, 
                                     failed=failed_count, 
                                     duplicates=duplicate_count)

        for i in range(start_index, end_index):
            row = df.iloc[i]
            contact = format_phone_number(row['phone'])

            if contact in log["successful"] or contact in log["failed"]:
                log["duplicates"].append(contact)
                duplicate_count += 1
                progress_bar.update(task, advance=1, duplicates=duplicate_count)
                continue

            message = message_template
            for column in df.columns:
                message = message.replace(f"{{{{{column}}}}}", row[column])

            success = send_message(contact, message)

            if success:
                log["successful"].append(contact)
                successful_count += 1
                progress_bar.update(task, advance=1, successful=successful_count)
            else:
                log["failed"].append(contact)
                failed_count += 1
                progress_bar.update(task, advance=1, failed=failed_count)

            # Update progress
            progress["last_processed"] = int(i)  # Ensure this is a standard Python int
            save_progress(progress)
            save_log(log)

    print("Batch processing completed.")
    print(f"Summary:\nSuccessful: {successful_count}\nFailed: {failed_count}\nDuplicates: {duplicate_count}")
    if end_index == total and os.path.exists('progress.json'):
        os.remove('progress.json')

# Set delay for waiting
delay = 30

# Set up WebDriver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print('Once your browser opens up sign in to web whatsapp')
driver.get('https://web.whatsapp.com')
input("AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER...")

# Check for resuming
if os.path.exists('progress.json'):
    resume = input("A previous session was found. Do you want to resume from where it left off? (yes/no): ").strip().lower()
    if resume == 'yes':
        pass
    else:
        os.remove('progress.json')

# Get the number of contacts to process in this batch
batch_size = int(input("Enter the number of contacts to process in this batch: ").strip())

main(batch_size)

# Close the driver
driver.quit()
