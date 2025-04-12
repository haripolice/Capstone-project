import mysql.connector
import pandas as pd

# TiDB Connection
connection = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="3wKrzSV6FDpedz7.root",
    password="UU1J4UQ08VQ0aZnT",
    database="guvi"
)
cursor = connection.cursor()

# Create "IMBD" Table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS IMBD (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255),    
    genre VARCHAR(100),
    ratings FLOAT,
    voting_counts INT,
    duration INT
);
""")
connection.commit()

# Load the IMDb 2024 dataset
df = pd.read_csv("IMDb_2024_Movies.csv")

# Convert NaN values to None for SQL insertion
df = df.where(pd.notnull(df), None)

# Insert data into TiDB "IMBD" table
for _, row in df.iterrows():
    sql = """
    INSERT INTO IMBD (movie_name, genre, ratings, voting_counts, duration)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (row["Movie Name"], row["Genre"], row["Ratings"], row["Voting Counts"], row["Duration"])
    
    cursor.execute(sql, values)

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("✅ Data successfully stored in TiDB 'IMBD' table!")
