import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Quick check for API keys (for debugging)
if not OPENWEATHER_API_KEY:
    print("Warning: OPENWEATHER_API_KEY not found in .env file!")
if not NEWS_API_KEY:
    print("Warning: NEWS_API_KEY not found in .env file!")

class WeatherNewsDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyGlance")
        self.root.geometry("850x950")

        self.title_label = tk.Label(self.root, text="Welcome to PyGlance - Your Daily Weather & News Update", font=("Arial",20)).pack(pady=10)

        # City entry
        tk.Label(self.root, text="Enter City:").pack(pady=5)
        self.city_entry = tk.Entry(self.root, width=50)
        self.city_entry.pack()
        self.city_entry.insert(0, "London") # Default city

        # News category entry
        tk.Label(self.root, text="Enter News Category (e.g., general, sports, technology):").pack(pady=5)
        self.news_category_entry = tk.Entry(self.root, width=50)
        self.news_category_entry.pack()
        self.news_category_entry.insert(0, "general") # Default category

        # Email sender entry
        tk.Label(self.root, text="Enter Sender Email:").pack(pady=5)
        self.email_sender_entry = tk.Entry(self.root, width=50)
        self.email_sender_entry.pack()

        # Email password entry
        tk.Label(self.root, text="Enter Email Password:").pack(pady=5)
        self.email_password_entry = tk.Entry(self.root, width=50, show="*")
        self.email_password_entry.pack()

        # Email receiver entry
        tk.Label(self.root, text="Enter Receiver Email:").pack(pady=5)
        self.email_receiver_entry = tk.Entry(self.root, width=50)
        self.email_receiver_entry.pack()

        # SMTP server entry
        tk.Label(self.root, text="Enter SMTP Server (e.g., smtp.gmail.com):").pack(pady=5)
        self.smtp_server_entry = tk.Entry(self.root, width=50)
        self.smtp_server_entry.pack()
        self.smtp_server_entry.insert(0, "smtp.gmail.com")

        # SMTP port entry
        tk.Label(self.root, text="Enter SMTP Port:").pack(pady=5)
        self.smtp_port_entry = tk.Entry(self.root, width=50)
        self.smtp_port_entry.pack()
        self.smtp_port_entry.insert(0, "587")

        # Fetch button
        self.fetch_button = tk.Button(self.root, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack(pady=10)

        # Weather display
        tk.Label(self.root, text="Weather:").pack()
        self.weather_text = scrolledtext.ScrolledText(self.root, width=70, height=5, wrap=tk.WORD)
        self.weather_text.pack(pady=5)

        # News display
        tk.Label(self.root, text="News:").pack()
        self.news_text = scrolledtext.ScrolledText(self.root, width=70, height=15, wrap=tk.WORD)
        self.news_text.pack(pady=5)

        # Send email button
        self.send_email_button = tk.Button(self.root, text="Send Email Update Now", command=self.send_email)
        self.send_email_button.pack(pady=10)

        # Start daily email thread
        self.start_daily_email_thread()

        # Start the GUI event loop
        self.root.mainloop()

    def fetch_weather(self, city):
        if not OPENWEATHER_API_KEY:
            raise Exception("OPENWEATHER_API_KEY is missing. Please add it to your .env file.")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            return f"Weather in {city}: {weather_desc}, Temperature: {temp}°C, Humidity: {humidity}%"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception(f"City '{city}' not found. Please check the spelling or try another city.")
            raise Exception(f"Error fetching weather: {str(e)}")
        except (KeyError, json.JSONDecodeError):
            raise Exception("Error parsing weather data.")

    def fetch_news(self, category):
        if not NEWS_API_KEY:
            raise Exception("NEWS_API_KEY is missing. Please add it to your .env file.")
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            articles = data['articles'][:5]  # Get top 5 articles
            news_str = ""
            for article in articles:
                title = article['title']
                source = article['source']['name']
                desc = article['description'] or "No description available."
                news_str += f"{title} - {source}\n{desc}\n\n"
            return news_str.strip() if news_str else "No news articles found."
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception(f"Category '{category}' not found or invalid. Please check the spelling or try another category (e.g., general, sports, technology).")
            raise Exception(f"Error fetching news: {str(e)}")
        except (KeyError, json.JSONDecodeError):
            raise Exception("Error parsing news data.")

    def fetch_data(self):
        city = self.city_entry.get().strip()
        category = self.news_category_entry.get().strip()
        if not city or not category:
            messagebox.showerror("Error", "Please enter a city and news category.")
            return
        try:
            weather = self.fetch_weather(city)
            news = self.fetch_news(category)
            self.weather_text.delete(1.0, tk.END)
            self.weather_text.insert(tk.END, weather)
            self.news_text.delete(1.0, tk.END)
            self.news_text.insert(tk.END, news)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_email(self):
        sender = self.email_sender_entry.get().strip()
        password = self.email_password_entry.get()
        receiver = self.email_receiver_entry.get().strip()
        smtp_server = self.smtp_server_entry.get().strip()
        smtp_port_str = self.smtp_port_entry.get().strip()
        city = self.city_entry.get().strip()
        category = self.news_category_entry.get().strip()

        if not all([sender, password, receiver, smtp_server, smtp_port_str, city, category]):
            messagebox.showerror("Error", "Please fill in all email and data fields.")
            return

        try:
            smtp_port = int(smtp_port_str)  # Convert port to integer
            weather = self.fetch_weather(city)
            news = self.fetch_news(category)
            subject = f"Daily Weather & News Update - {datetime.date.today()}"
            body = f"{weather}\n\nNews:\n{news}"

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()

            messagebox.showinfo("Success", "Email sent successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid SMTP port number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def daily_email_thread(self):
        while True:
            now = datetime.datetime.now(datetime.timezone.utc) 
            # Calculate seconds until next 8:00 AM IST
            tomorrow = now + datetime.timedelta(days=1)
            next_send = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 8, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
            seconds_until = (next_send - now).total_seconds()
            time.sleep(seconds_until)
            self.send_email()

    def start_daily_email_thread(self):
        thread = threading.Thread(target=self.daily_email_thread, daemon=True)
        thread.start()

# Start the application
if __name__ == "__main__":
    app = WeatherNewsDashboard()
