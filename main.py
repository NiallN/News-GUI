__author__ = "Niall Nolan"
__version__ = "1.0.0"


import tkinter as tk
import requests
import socket


def api_call(url):
    """
    Retrieves results of an API call.
    :param url: Enter an API url with API key.
    :param row:
    :param col:
    :param sticky:
    :return: news_articles
    """
    try:
        news = requests.get(url)
        news = news.json()
        return news

    except socket.error:
        no_connection_label = tk.Label(window, text="No internet connection. \nPlease address and re-open this program later.", font=("bold", 22), pady=20)
        no_connection_label.grid(row=0, column=1, padx=10, pady=75, sticky=tk.N)


def retrieve_article_titles(news):
    # Retrieve the news article titles from API call.
    news_articles = []
    for item in news["articles"]:
        news_articles.append(item["title"])
    return news_articles


def create_news_widget(row, col, sticky):
    """
    Creates a news widget.
    :param row: Select grid row, e.g. 0
    :param col: Select grid column, e.g. 1.
    :param sticky: Select sticky position, e.g. tk.W.
    :param articles: Feed in news articles.
    :return: news_widget
    """
    # Create news widget.
    news_widget = tk.Listbox(window, border=1)
    news_widget.grid(row=row, column=col, sticky=sticky)
    return news_widget


def create_vertical_scrollbar(row, col, ipady, sticky, news_widget):
    """
    Creates a Y-axis scrollbar for a new widget listbox.
    :param row: Select grid row, e.g. 0
    :param col: Select grid column, e.g. 1.
    :param ipady: Select the amount of internal padding.
    :param sticky: Select sticky position, e.g. tk.W.
    :param news_widget:
    :return:
    """
    news_y_scrollbar = tk.Scrollbar(window, orient="vertical")
    news_y_scrollbar.grid(row=row, column=col, ipady=ipady, sticky=sticky)
    news_y_scrollbar.configure(command=news_widget.yview)
    news_widget.configure(yscrollcommand=news_y_scrollbar.set)


def insert_article_titles(news_articles, widget):
    """
    Is used by 'keyword_entry_button' as its' command parameter.
    :return: News article titles from a keyword search.
    """
    for item in news_articles:
        widget.insert(2, item)


def keyword_articles():
    """
    Retrieves articles relevant to user's keyword input.
    :return:
    """
    # To retrieve user's keyword, use "keyword.get()".
    # Retrieve the keyword news.
    keyword_news = api_call("http://newsapi.org/v2/top-headlines?language=en&q=" + keyword.get() + "&apiKey=c0cbc3a185e84d60bf612e355c9a2760")

    # Retrieve the keyword news article titles.
    keyword_news_article_titles = retrieve_article_titles(keyword_news)

    # Clear the keyword_news_widget listbox from any previous uses.
    keyword_news_widget.delete(0, "end")

    keyword_news_widget.insert(1, "Keyword is " + str(keyword.get()) + " and the number of relevant articles is " + str(keyword_news["totalResults"]) + ".", "")

    # Populate the widget with keyword news article titles.
    insert_article_titles(keyword_news_article_titles, keyword_news_widget)

    # Clear the keyword entry field.
    keyword_entry_field.delete(0, "end")


# Create window object.
window = tk.Tk()
# Title the window.
window.title("The News")
# Set base height & width of the window.
window.geometry("1200x850")

# TODO: Figure it out!
window.grid_columnconfigure(1, weight=1, uniform="foo")

# Create labels for each news section.
ireland_news_label = tk.Label(window, text="Irish News:", font=("bold", 14), pady=20)
world_news_label = tk.Label(window, text="World News:", font=("bold", 14), pady=20)
keyword_news_label = tk.Label(window, text="Keyword News:", font=("bold", 14), pady=20)
weather_label = tk.Label(window, text="Weather Forecast:", font=("bold", 14), pady=20)

# Use a grid format to organise the layout of the window.
ireland_news_label.grid(row=0, column=0, padx=10, pady=75, sticky=tk.W)
world_news_label.grid(row=1, column=0, padx=10, pady=75, sticky=tk.W)
keyword_news_label.grid(row=2, column=0, padx=10, pady=75, sticky=tk.W)
weather_label.grid(row=3, column=0, padx=10, pady=50, sticky=tk.W)


# Irish News:

# News API call valid parameters: sources, q, language, country, category.
# For country news, include e.g. "country=ie". Additional category is e.g. "country=ie&categories=business".
# Retrieve Irish news from the API.
ireland_news = api_call("http://newsapi.org/v2/top-headlines?country=ie&apiKey=c0cbc3a185e84d60bf612e355c9a2760")

# Retrieve Irish news article titles.
ireland_news_article_titles = retrieve_article_titles(ireland_news)

# Call create_news_widget() to create an Irish news widget.
ireland_news_widget = create_news_widget(0, 1, tk.W + tk.E)
# Call create_vertical_scrollbar() to create a Y-axis scrollbar on the ireland_news_widget.
create_vertical_scrollbar(0, 2, 55, tk.E, ireland_news_widget)

# Populate the widget with Irish article titles.
insert_article_titles(ireland_news_article_titles, ireland_news_widget)


# World News:

# News API call valid parameters: sources, q, language, country, category.
# For news categories, include e.g. "categories=business".
# Retrieve World news (technically all English language news) from the API.
world_news = api_call("http://newsapi.org/v2/top-headlines?language=en&apiKey=c0cbc3a185e84d60bf612e355c9a2760")

# Retrieve World news article titles.
world_news_article_titles = retrieve_article_titles(world_news)

# Call create_news_widget() to create a World news widget.
world_news_widget = create_news_widget(1, 1, tk.W + tk.E)
# Call create_vertical_scrollbar() to create a Y-axis scrollbar on the world_news_widget.
create_vertical_scrollbar(1, 2, 55, tk.E, world_news_widget)

# Populate the widget with World article titles.
insert_article_titles(world_news_article_titles, world_news_widget)


# User Keyword News:

# Create a label with instructions for the user to enter a keyword.
keyword_news_label = tk.Label(window, text="Type a keyword below and press ENTER to return relevant news:")
keyword_news_label.grid(row=2, column=1, sticky=tk.NW)

# Retrieve user's keyword input as a StringVar. TK monitors it for change allowing user re-use.
keyword = tk.StringVar()
# Save user input as 'textvariable' to bind it to 'keyword_entry_field'.
keyword_entry_field = tk.Entry(window, textvariable=keyword)
keyword_entry_field.grid(row=2, column=1, pady=20, sticky=tk.NW+tk.E)

# Clear Input
keyword_entry_button = tk.Button(window, text="ENTER", command=keyword_articles)
keyword_entry_button.grid(row=2, column=1, pady=35, sticky=tk.NW+tk.E)

# Display keyword news in a widget.
keyword_news_widget = create_news_widget(2, 1, tk.SW+tk.SE)

# Call create_vertical_scrollbar() to create a Y-axis scrollbar on the keyword_news_widget.
create_vertical_scrollbar(2, 2, 55, tk.E, keyword_news_widget)


# The Weather Forecast:

# Weather API call to openweathermap.org. My API key: 852b0537f775526e02999aca6fc779ce.
weather_data = api_call("http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&APPID=852b0537f775526e02999aca6fc779ce")

main_description = weather_data["weather"][0]["description"]
temp_kelvin = weather_data["main"]["temp"]
feels_like_kelvin = weather_data["main"]["feels_like"]
temp_celsius = temp_kelvin - 273.15
feels_like_celsius = feels_like_kelvin - 273.15
wind_speed = weather_data["wind"]["speed"]
wind_deg = weather_data["wind"]["deg"]

# Call create_news_widget() to create a Weather Forecast widget.
weather_widget = create_news_widget(3, 1, tk.W+tk.E)
# Call create_vertical_scrollbar() to create a Y-axis scrollbar on the world_news_widget.
create_vertical_scrollbar(3, 2, 55, tk.E, weather_widget)

# Populate the widget with Weather forecast.
weather_widget.insert(1, "Weather situation in Dublin is: " + main_description + ". The temperature is: " + str(int(temp_celsius)) + "°C. It feels like: " + str(int(feels_like_celsius)) + "°C.")
weather_widget.insert(2, "Wind speed is: " + str(wind_speed) + " with a direction of : " + str(wind_deg) + "°.", "")

# Populate the widget with Weather article titles.
# insert_article_titles(world_news_article_titles, world_news_widget)
weather_news = api_call("http://newsapi.org/v2/top-headlines?q=weather&apiKey=c0cbc3a185e84d60bf612e355c9a2760")

# Retrieve weather related article titles.
weather_news_article_titles = retrieve_article_titles(weather_news)

# Populate the widget with World article titles.
insert_article_titles(weather_news_article_titles, weather_widget)

# Open app window and keep it open.
window.mainloop()

