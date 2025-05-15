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