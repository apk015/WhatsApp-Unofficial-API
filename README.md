

# 📱 WhatsApp Unofficial API

Welcome to the **WhatsApp Unofficial API** project! This repository contains a powerful Python script to automate sending WhatsApp messages in bulk. Personalize your messages and reach your contacts with ease.

---

## 🌟 Features

- **📇 Read Contacts:** Import contacts from a CSV file.
- **✉️ Message Template:** Customize your message with placeholders.
- **📜 Logging:** Detailed logging for tracking and debugging.
- **🚀 Error Handling:** Robust error handling for smooth operation.
- **⏳ Progress Tracking:** Monitor the progress of message sending with a dynamic progress bar.
- **🔄 Resume Support:** Resume from where you left off in case of interruptions.
- **🖼️ Attachments:** Optionally send images or files with your messages.
- **📂 Graceful Shutdown:** Handles interruptions like `CTRL+C` and saves progress for resuming later.

---

## 🛠️ Requirements

Ensure you have the following installed:

- **Python 3.x**
- `pandas` library
- `selenium` library
- `webdriver_manager` library
- `rich` library
- **ChromeDriver**: Ensure that you have ChromeDriver installed. You can download it [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

---

## 📥 Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/apk015/WhatsApp-Unofficial-API.git
    cd whatsapp_unofficial_api
    ```

2. **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure `.env` file:**
   Create a `.env` file in the root of the project with the following content:
    ```ini
    CHROMEDRIVER_PATH=/path/to/your/chromedriver
    USER_DATA_DIR=/path/to/your/chrome_user_data
    LOG_FILE=whatsapp_unofficial_api.log
    CONTACTS_CSV=contacts.csv
    ```

   - Replace `/path/to/your/chromedriver` with the actual path where you installed ChromeDriver.
   - Replace `/path/to/your/chrome_user_data` with your Chrome profile path for WhatsApp Web.

---

## 📋 Usage

1. **Add Contacts:**

    Update the `contacts.csv` file with your contacts in the following format:

    ```csv
    Phone,Name
    1234567890,Alice
    0987654321,Bob
    1122334455,Charlie
    ```

2. **Customize Message:**

    Edit the `msg.txt` file to create your message template. Use `{{Name}}` as a placeholder for the contact's name and any other variables you want to personalize. For example, if your CSV contains a `City` column, you can use `{{City}}` in your message:

    ```txt
    Hi *{{Name}}*,
    I hope you're doing well in {{City}}!
    ```

    You can use any variable by inserting it within `{{variable_name}}` in the message template.

3. **Run the Script:**

    Execute the script to start sending messages:

    ```bash
    python main.py --batch-size 20 --image /path/to/image.jpg
    ```

    If you don’t want to send an image, simply omit the `--image` argument:

    ```bash
    python main.py --batch-size 20
    ```

4. **Sign In to WhatsApp Web:**

    After running the script, a Chrome browser will open. Sign in to WhatsApp Web and press ENTER in the terminal once your chats are visible.

5. **Batch Processing:**

    Enter the number of contacts to process in this batch when prompted. The script will handle the rest, sending messages in batches.

---

## 📂 Directory Structure

```
whatsapp_unofficial_api/
│
├── main.py
├── contacts.csv
├── msg.txt
├── .env
├── README.md
└── requirements.txt
```

---

## 📝 Logging and Progress

All activities are logged in `whatsapp_unofficial_api.log`. Check this file for detailed execution logs.

Progress is saved in `progress.json`. This allows you to resume from where you left off in case of any interruptions.

---

## 📌 Notes

- Ensure your computer has an active internet connection.
- WhatsApp Web should be open and logged in on your default browser.
- The script includes a 5-second delay between messages to avoid rate limits. Adjust if necessary.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## 📧 Contact

For any questions or issues, please [open an issue](https://github.com/apk015/WhatsApp-Unofficial-API/issues) on GitHub or contact us at **4apk015@gmail.com**.

---

## 🔍 Detailed Explanation

### Script Overview

The script automates the sending of WhatsApp messages using Selenium. It reads contacts from a CSV file and sends personalized messages based on a template from a text file. It can also optionally attach an image to the message.

### Key Variables

- **`options`**: Configures Chrome options for Selenium.
- **`delay`**: Time in seconds to wait for WhatsApp elements to load.
- **`batch_size`**: Number of contacts to process in each batch.

### Functions

- **`load_data()`**: Loads and processes the contacts CSV file.
- **`load_log()` & `save_log()`**: Manages logging of successful, failed, and duplicate messages.
- **`load_progress()` & `save_progress()`**: Tracks and saves progress of message sending.
- **`format_phone_number(phone)`**: Formats phone numbers by removing non-digit characters and leading zeros.
- **`send_message(contact, message, image_path=None)`**: Sends a WhatsApp message with or without an image using Selenium.

### Benefits

- **Efficiency**: Automates bulk messaging, saving time and effort.
- **Personalization**: Customizes messages for each contact.
- **Reliability**: Provides detailed logging and error handling to ensure smooth operation.
- **Flexibility**: Allows resuming from where you left off, handling interruptions gracefully.
- **Attachments**: You can attach images or files when sending messages.

---

## 💻 Example Usage

1. **Prepare your data**:
    - Ensure your `contacts.csv` file is filled with the contacts you want to message.
    - Customize the `msg.txt` file to include your desired message with placeholders for personalization.

2. **Run the script**:
    ```bash
    python main.py --batch-size 20 --image /path/to/image.jpg
    ```

3. **Sign in to WhatsApp Web** when the browser opens and press ENTER in the terminal to start the messaging process.

4. **Monitor progress**: The script will display a progress bar and log details of the messaging process.

---

## 🔧 Troubleshooting

- **Log File Corruption**: If the log file is corrupted, the script will recreate it to avoid interruptions.
- **Progress File Corruption**: If the progress file is corrupted, the script will start from the beginning.
- **Missing .env file**: Make sure to configure `.env` properly with the correct paths to your ChromeDriver and Chrome user data.

For further assistance, feel free to [open an issue](https://github.com/apk015/WhatsApp-Unofficial-API/issues).

