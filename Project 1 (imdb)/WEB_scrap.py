from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# IMDb 2024 Movies URL
URL = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"

# Correct ChromeDriver path
chrome_driver_path = r"C:\Users\KRHA1002\OneDrive - Nielsen IQ\Profile\GUVI\chrome-win64\chromedriver-win64\chromedriver.exe"

# Set up Selenium WebDriver with user-agent
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)

# Open IMDb page
driver.get(URL)
time.sleep(10)  # Increase wait time

# Wait for movies to load
WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'lister-item')]")))

# Scraping movie details
movies = driver.find_elements(By.XPATH, "//div[contains(@class, 'lister-item')]")
print(f"Movies found: {len(movies)}")  # Debugging: Check if movies are found

movie_list = []
for movie in movies:
    try:
        name = movie.find_element(By.TAG_NAME, "h3").text
    except:
        name = "Unknown"
    try:
        genre = movie.find_element(By.CLASS_NAME, "genre").text.strip()
    except:
        genre = "Unknown"
    try:
        rating = movie.find_element(By.CLASS_NAME, "ratings-imdb-rating").text
    except:
        rating = None
    try:
        votes = movie.find_element(By.XPATH, ".//span[@name='nv']").text.replace(",", "")
    except:
        votes = None
    try:
        duration = movie.find_element(By.CLASS_NAME, "runtime").text.replace(" min", "")
    except:
        duration = None
    
    movie_list.append([name, genre, rating, votes, duration])

# Close the browser
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(movie_list, columns=["Movie Name", "Genre", "Ratings", "Voting Counts", "Duration"])

# Save CSV
df.to_csv("IMDb_2024_Movies.csv", index=False, encoding="utf-8-sig")
print("✅ Data Scraped and Saved!")
