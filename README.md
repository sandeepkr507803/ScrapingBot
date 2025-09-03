# ScrapingBot

### 1. Project Overview

This project is a Web Scraping Chatbot that:
* Uses Selenium + BeautifulSoup to scrape the content of any given website.
* Cleans and lemmatizes the text with NLTK to normalize words.
* Sends the processed text as context to Groq’s LLM (meta-llama/llama-4-scout-17b-16e-instruct) using the OpenAI-compatible API.
* Provides a Streamlit chat interface where users can ask questions about the scraped site.

### 2. Setup Instructions

Step 1: Clone the repo
- git clone https://github.com/your-username/WebScrapingChatbot.git
- cd WebScrapingChatbot

Step 2: Install dependencies
- pip install -r requirements.txt

Step 3: Configure environment variables
Create a .env file in the project root with:
- GROQ_API_KEY=your_groq_api_key_here

Step 4: Run the app
- streamlit run app.py

### 3. Usage

- Enter the website URL in the text box.
- The app will scrape and preprocess the content.
- Start chatting with the bot in the Streamlit interface.
- The bot will answer based on the scraped site content.

### 4. Key Functions

- get_driver() → Launches headless Chrome with Selenium.
- scrape_website(url) → Scrapes and cleans webpage text.
- lemmatize_text(text) → Normalizes words using NLTK.
- ask_groq(context, question) → Sends context + question to Groq API and returns response.

### 5. Notes

- Requires Chrome and ChromeDriver installed (unless using webdriver-manager).
- Some Chrome logs like DevTools listening or DEPRECATED_ENDPOINT are harmless.
- Replace the model name if Groq changes it in the future (check their docs).
