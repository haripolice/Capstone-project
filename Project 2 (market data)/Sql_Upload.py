import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load dataset
df = pd.read_csv("IMDb_2024_Movies.csv")

# Convert columns to proper data types
df["Ratings"] = pd.to_numeric(df["Ratings"], errors="coerce")
df["Voting Counts"] = pd.to_numeric(df["Voting Counts"], errors="coerce")
df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce")

# Top 10 Movies by Ratings
top_movies = df.nlargest(10, "Ratings")

plt.figure(figsize=(10,5))
sns.barplot(x="Ratings", y="Movie Name", data=top_movies, palette="viridis")
plt.title("Top 10 Movies by Rating (2024)")
plt.xlabel("IMDb Rating")
plt.ylabel("Movie Name")
plt.show()

# Genre Distribution
plt.figure(figsize=(10,5))
sns.countplot(y="Genre", data=df, order=df["Genre"].value_counts().index, palette="coolwarm")
plt.title("Movies Count per Genre (2024)")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.show()
