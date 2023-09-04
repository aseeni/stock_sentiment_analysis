import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tkinter as tk
from textblob import TextBlob
import yfinance as yf
from datetime import datetime
import json, sys

#url = "https://www.fool.com/earnings/call-transcripts/2023/02/02/apple-aapl-q1-2023-earnings-call-transcript/"

def fetch_transcript():
    url = url_entry.get()
    response = requests.get(url)
    transcript_html = response.text
    soup = BeautifulSoup(transcript_html, "html.parser")

    included_class = "tailwind-article-body"
    excluded_class = "article-pitch-container"

    transcript_element = soup.find_all("div", class_= included_class)


    for element in transcript_element:
        exclude_elements = element.find_all(class_ = excluded_class)

        for excluded_element in exclude_elements:
            excluded_element.extract()

    transcript_text = ""

    for element in transcript_element:
        transcript_text += element.get_text() + "\n"

    # perform sentiment analysis
    blob = TextBlob(transcript_text)
    sentiment_score = blob.sentiment.polarity
    print("Sentiment analysis score: ", sentiment_score)
        
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(transcript_text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def stock_price_change():
    quarter = quarter_entry.get().upper()
    start_date = ""
    end_date = ""

    if quarter == "Q1":
        start_date = "2023-01-01"
        end_date = "2023-03-31"

    elif quarter == "Q2":
        start_date = "2023-04-01"
        end_date = "2023-06-30"
    
    elif quarter == "Q3":
        start_date = "2023-07-01"
        end_date = "2023-09-30"
    
    elif quarter == "Q4":
        start_date = "2023-10-01"
        end_date = "2023-12-31"
    
    else:
        return "Invalid quarter entered"

    ticker_from_user = ticker_entry.get().upper()
    ticker = yf.Ticker(ticker_from_user)
    ticker_history = ticker.history(start=start_date, end=end_date)

    print(ticker_history)
    
    quarter_start_stock_price = ticker_history.loc[:, "Open"][0]
    quarter_end_stock_price = ticker_history.loc[:, "Close"][-1]
    quarter_return = (quarter_end_stock_price - quarter_start_stock_price) * 100 / quarter_start_stock_price
    print("Return during requested quarter for %s : %d %%" % (ticker_from_user, quarter_return))

    return -1

def quit_app():
    root.destroy()

#create main window
root = tk.Tk()
root.title("Earnings Call Transcript Parser")

#Create UI components
url_label = tk.Label(root, text = "Enter Transcript URL from Motley Fool: ")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

fetch_button = tk.Button(root, text="Fetch Transcript", command=fetch_transcript)
fetch_button.pack()

# for the quarter
quarter_label = tk.Label(root, text = "\n\nEnter The Relevant Quarter e.g. Q1 or q1")
quarter_label.pack()

quarter_entry = tk.Entry(root, width=50)
quarter_entry.pack()

fetch_button = tk.Button(root, text="Fetch stock change in quarter")
fetch_button.pack()

# for the ticker
ticker_label = tk.Label(root, text = "\n\nEnter The Ticker")
ticker_label.pack()

ticker_entry = tk.Entry(root, width=50)
ticker_entry.pack()

fetch_button = tk.Button(root, text="Fetch ticker results in quarter", command=stock_price_change)
fetch_button.pack()

transcript_textbox = tk.Text(root, height=20, width=80)
transcript_textbox.pack()

quick_button = tk.Button(root, text="Quit", command = quit_app)
quick_button.pack()

# Start the GUI event loop
root.mainloop()