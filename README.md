# 📱 WhatsApp Unofficial API

Welcome to the **WhatsApp Unofficial API** project! This repository contains a powerful Python script to automate sending WhatsApp messages in bulk. Personalize your messages and reach your contacts with ease.

---

## 🌟 Features

- **📇 Read Contacts:** Import contacts from a CSV file.
- **✉️ Message Template:** Customize your message with placeholders.
- **🔧 Personalization:** Automatically personalize messages with contact names.
- **📜 Logging:** Detailed logging for tracking and debugging.
- **🚀 Error Handling:** Robust error handling for smooth operation.

---

## 🛠️ Requirements

Ensure you have the following installed:
- **Python 3.x**
- `pandas` library
- `pywhatkit` library

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

---

## 📋 Usage

1. **Add Contacts:**

    Update the `contacts.csv` file with your contacts in the following format:

    ```csv
    Name,Phone
    Alice,1234567890
    Bob,0987654321
    Charlie,1122334455
    ```

2. **Customize Message:**

    Edit the `msg.txt` file to create your message template. Use `{{Name}}` as a placeholder for the contact's name:

    ```txt
    hi *{{Name}}*
    I hope you're doing well!
    ```

3. **Run the Script:**

    Execute the script to start sending messages:

    ```bash
    python main.py
    ```

---

## 📂 Directory Structure

```
whatsapp_unofficial_api/
│
├── main.py
├── contacts.csv
├── msg.txt
├── README.md
└── requirements.txt
```

---

## 📝 Logging

All activities are logged in `whatsapp_unofficial_api.log`. Check this file for detailed execution logs.

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
