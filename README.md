# 👀 PyGlance - Your Daily Weather & News Update

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)  
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-red.svg)  
![Requests](https://img.shields.io/badge/Requests-HTTP-blue?logo=python&logoColor=white)  
![OpenWeatherAPI](https://img.shields.io/badge/API-OpenWeather-orange?logo=cloud&logoColor=white)  
![NewsAPI](https://img.shields.io/badge/API-NewsAPI-yellow?logo=news&logoColor=black)  
![SMTP](https://img.shields.io/badge/Email-SMTP-green?logo=gmail&logoColor=white)  

PyGlance is a desktop application that provides real-time weather and news updates, along with the ability to send automated daily email updates to any user.

---

## ✨ Features

* 🌦 Weather Updates – Get current weather with temperature, humidity, and conditions
* 📰 News Headlines – Fetch top news by category (general, sports, technology, etc.)
* 📧 Email Notifications – Send daily reports (Weather + News) directly to your inbox
* ⏰ Auto-Scheduler – Automatic email delivery every morning at 8:00 AM IST
* 🖥️ User-Friendly GUI – Built with Tkinter and ScrolledText widgets
* 🔑 Environment Variables – Secure API keys and credentials via .env file

---

## 🛠️ Technologies Used

- ***Python*** 3.10+ – Core programming language
- ***Tkinter*** – For GUI development
- ***Requests*** – For API communication
- ***OpenWeatherAPI*** – For real-time weather updates
- ***NewsAPI*** – For top headlines and categories
- ***smtplib*** & ***email.mime*** – For sending structured emails
- ***threading*** & ***datetime*** – For scheduling daily tasks
- ***dotenv*** – For environment variable management

---

## ⚙️ Installation

1. **Clone this repository:**
    ```bash
    git clone https://github.com/OmKadane/PyGlance.git
    cd PyGlance
    ```
2. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```
3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Create a .env file in the project root with your API keys:**
    ```bash
    OPENWEATHER_API_KEY=your_openweather_api_key
    NEWS_API_KEY=your_newsapi_key
    ```

---

## 🏃‍♂️ Running the Application

Once the installation is complete, run the following command in your terminal:
```bash
python main.py
```
* **Enter your city and news category
* **Click Fetch Data to see updates
* **Configure email settings and click Send Email Update Now
* **Daily automated emails will be sent at 8:00 AM IST

---

## 🔮 Future Scope

* ✅ SMS Alerts – Integrate Twilio/Nexmo to send Weather + News as SMS
* ✅ Push Notifications – Desktop/mobile notifications for breaking news
* ✅ Multi-City Support – Track weather for multiple locations
* ✅ Advanced Scheduler – Customizable time slots for updates
* ✅ Cloud Sync – Save preferences and history in a database
* ✅ Dark Mode UI – Improved visual experience for night use
* ✅ Web Dashboard – Access PyGlance via browser
