import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tkinter as tk
from textblob import TextBlob

#url = "https://www.fool.com/earnings/call-transcripts/2023/02/02/apple-aapl-q1-2023-earnings-call-transcript/"

def fetch_transcript():
    url = url_entry.get()
    response = requests.get(url)
    transcript_html = response.text
    soup = BeautifulSoup(transcript_html, "html.parser")

    prepared_remarks = ""
    q_and_a = ""
    call_participants = ""

    included_class = "tailwind-article-body"
    #excluded_class = ["article-pitch-container", "image imgR"]
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
    print(sentiment_score)
        
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(transcript_text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

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

transcript_textbox = tk.Text(root, height=20, width=80)
transcript_textbox.pack()

quick_button = tk.Button(root, text="Quit", command = quit_app)
quick_button.pack()

# Start the GUI event loop
root.mainloop()