from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# IMDb 2024 Movies URL (Example - Update with the actual one)
URL = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"

# Set up Selenium WebDriver (Make sure to install the correct driver for your browser)
driver = webdriver.Chrome()

# Open IMDb page
driver.get(URL)
time.sleep(3)  # Wait for the page to load

# Scraping movie details
movies = driver.find_elements(By.CLASS_NAME, "list_item")

movie_list = []
for movie in movies:
    name = movie.find_element(By.TAG_NAME, "h4").text
    genre = movie.find_element(By.CLASS_NAME, "cert-runtime-genre").text.split("|")[-1].strip()
    try:
        rating = movie.find_element(By.CLASS_NAME, "rating").text
    except:
        rating = None
    try:
        votes = movie.find_element(By.CLASS_NAME, "votes").text.replace(",", "")
    except:
        votes = None
    try:
        duration = movie.find_element(By.CLASS_NAME, "runtime").text.replace(" min", "")
    except:
        duration = None
    
    movie_list.append([name, genre, rating, votes, duration])

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(movie_list, columns=["Movie Name", "Genre", "Ratings", "Voting Counts", "Duration"])

# Save CSV for each genre
for genre in df["Genre"].unique():
    df[df["Genre"] == genre].to_csv(f"{genre}_movies_2024.csv", index=False)

# Save full dataset
df.to_csv("IMDb_2024_Movies.csv", index=False)
print("Data Scraped and Saved!")
