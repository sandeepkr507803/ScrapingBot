# Import libraries
import os
import time
import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import nltk

# Download required NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet

# Load environment variables
load_dotenv()
import openai

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"


# Configure Selenium driver for Linux (Render)
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=options)


# Scrape function
def scrape_website(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    return soup.get_text(separator='\n', strip=True)


lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def lemmatize_text(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    lemmas = [lemmatizer.lemmatize(w, get_wordnet_pos(p)) for w, p in pos_tags]
    return " ".join(lemmas)


def ask_groq(context, question):
    prompt = f"""You are a smart assistant. Use the website content below to answer:

Website Content:
\"\"\"{context}\"\"\"

Question: {question}
Answer:"""
    client = openai.OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3,
    )
    return response.choices[0].message.content


# Streamlit UI
st.set_page_config(page_title="Web Scraping Chatbot", page_icon="🤖")
st.title("🤖 Web Scraping Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "lemmatized_text" not in st.session_state:
    st.session_state.lemmatized_text = None

with st.form("url_form"):
    url = st.text_input("Enter URL to scrape", "")
    submitted = st.form_submit_button("Scrape Website")
    if submitted and url:
        with st.spinner("Scraping and processing..."):
            raw_text = scrape_website(url)
            st.session_state.lemmatized_text = lemmatize_text(raw_text)
            st.session_state.chat_history = []
        st.success("Website scraped and lemmatized! Start chatting below.")

if st.session_state.lemmatized_text:
    st.markdown("**Chat with the bot below:**")
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        else:
            st.chat_message("assistant").write(chat["content"])

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Bot is typing..."):
            response = ask_groq(st.session_state.lemmatized_text, user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
