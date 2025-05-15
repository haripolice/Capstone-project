# Action movies 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.imdb.com/search/title/?title_type=feature&genres=action&release_date=2024-01-01,2024-12-31")

time.sleep(3)  # Waiting for the page to load

genre = "Action"

# Scroll Until No More New Data Loads
scrolling = True
movies_per_page = 50  # Assuming each load gives 50 movies
total_movies_needed = 500
current_movies = 0

while scrolling and current_movies < total_movies_needed:
    old_page_source = driver.page_source  # Save old page source
    
    # Scroll down to load more data
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Allow time for new data to load
    
    new_page_source = driver.page_source  # Save new page source

    if new_page_source == old_page_source:
        try:
            # Locate and click the "See More" button if present
            see_more_button = driver.find_element(By.XPATH, "//span[contains(@class, 'ipc-see-more')]")
            ActionChains(driver).move_to_element(see_more_button).click().perform()
            time.sleep(2)  # Wait for new content to load
        except Exception:
            scrolling = False  # Stop scrolling if button isn't found
    else:
        current_movies += movies_per_page  # Increment count

# Extract movie containers
movie_blocks = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

movies_list = []

for movie in movie_blocks:
    try:
        title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.strip()
    except:
        title = "N/A"

    try:
        duration_element = movie.find_element(By.XPATH, ".//span[contains(@class, 'dli-title-metadata-item') and (contains(text(),'h') or contains(text(),'m'))]")
        duration = duration_element.text.strip() if duration_element.text.strip() else "N/A"
    except:
        duration = "N/A"

    try:
        rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text.strip()
    except:
        rating = "N/A"

    try:
        voting = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.strip()
    except:
        voting = "N/A"

    movie_data = {
        "Title": title,
        "Genre": genre,
        "Duration": duration,
        "Rating": rating,
        "Voting": voting,
    }
    movies_list.append(movie_data)

# Print results
for movie in movies_list:
    print(movie)

# Close the driver
driver.quit()

#common csv converting code

import pandas as pd


df=pd.DataFrame(movies_list)
# Cleaning Steps:
# 1. Remove leading numbers from "Title"
df["Title"] = df["Title"].str.replace(r"^\d+\.\s*", "", regex=True)

# 2. Remove parentheses from "Voting"
df["Voting"] = df["Voting"].str.replace(r"[()]", "", regex=True)

# 3. Reset index to start from 1
df.index = df.index + 1

df.to_csv(r"action.csv", index=False, encoding="utf-8")
print("CSV file saved successfully in D:\\Guvi Ds!")


*
*
*


# Comedy movies
from selenium import webdriver