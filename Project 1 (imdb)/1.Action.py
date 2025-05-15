import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Define list of genres to scrape
genres = ["action", "comedy", "drama", "thriller", "romance", "horror"]

# Chrome WebDriver setup
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

for genre in genres:
    print(f"\n🔍 Scraping genre: {genre.capitalize()} (limit 200 movies)")

    driver = webdriver.Chrome(options=options)
    url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres={genre}"
    driver.get(url)
    time.sleep(5)

    # Click "Load More" button up to 3 times (50*4 = 200 max)
    def click_load_more_limited(max_clicks=4):
        clicks = 0
        while clicks < max_clicks:
            try:
                load_more_button = driver.find_element(By.XPATH,
                    '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button')
                ActionChains(driver).move_to_element(load_more_button).perform()
                load_more_button.click()
                print(f"Clicked 'Load More' ({clicks + 1}/{max_clicks})")
                clicks += 1
                time.sleep(3)
            except Exception:
                print("No more 'Load More' button available.")
                break

    click_load_more_limited()

    # Extract movie cards (limit to 200)
    movie_lists = driver.find_elements(By.XPATH,
        '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li')[:200]

    print(f"🎬 Extracting {len(movie_lists)} movies...")

    titles = []
    ratings = []
    votings = []
    durations = []

    for movie in movie_lists:
        try:
            title = movie.find_element(By.XPATH, './/h3').text
            rating = movie.find_element(By.XPATH, './/span[contains(@class,"ratingGroup")]/span[1]').text
            voting = movie.find_element(By.XPATH, './/span[contains(@class,"ratingGroup")]/span[2]').text
            duration = movie.find_element(By.XPATH, './/span[contains(text(),"h") or contains(text(),"m")]').text

            titles.append(title)
            ratings.append(rating)
            votings.append(voting)
            durations.append(duration)
        except Exception:
            continue

    df = pd.DataFrame({
        'Title': titles,
        'Genre': genre.capitalize(),
        'Rating': ratings,
        'Voting': votings,
        'Duration': durations
    })

    csv_filename = f"{genre.capitalize()}_IMDb_2024.csv"
    df.to_csv(csv_filename, index=False)
    print(f"💾 Saved {len(df)} movies to {csv_filename}")

    driver.quit()

import pandas as pd
import glob

# Collect all genre CSV files
csv_files = glob.glob("*_IMDb_2024.csv")

# List to store dataframes
dfs = []

# # Read and append each CSV
# for file in csv_files:
#     print(f"📥 Loading: {file}")
#     df = pd.read_csv(file)
#     dfs.append(df)

# # Concatenate all dataframes
# combined_df = pd.concat(dfs, ignore_index=True)

# # Save to one consolidated CSV
# combined_df.to_csv("IMDb_2024_All_Genres.csv", index=False)
# print("✅ All genres consolidated into: IMDb_2024_All_Genres.csv")


import mysql.connector
import pandas as pd

# 1. Read the combined CSV
df = pd.read_csv("IMDb_2024_All_Genres.csv")

# 2. Connect to TiDB Cloud MySQL
connection = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="3wKrzSV6FDpedz7.root",
    password="yz4hy5chwUbQgR1s",
    database="guvi"
)


mycursor = connection.cursor(buffered=True)

# 3. Create the table if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS IMDB (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Genre VARCHAR(50),
    Rating VARCHAR(10),
    Voting VARCHAR(50),
    Duration VARCHAR(50)
)
"""
mycursor.execute(create_table_query)

# 4. Insert data into the table
insert_query = """
INSERT INTO IMDB (Title, Genre, Rating, Voting, Duration)
VALUES (%s, %s, %s, %s, %s)
"""

for index, row in df.iterrows():
    mycursor.execute(insert_query, (
        row['Title'],
        row['Genre'],
        row['Rating'],
        row['Voting'],
        row['Duration']
    ))

# 5. Commit and close
connection.commit()
print("✅ Data inserted into TiDB table 'IMDB' successfully.")
mycursor.close()
connection.close()
# 6. Read from the table to verify