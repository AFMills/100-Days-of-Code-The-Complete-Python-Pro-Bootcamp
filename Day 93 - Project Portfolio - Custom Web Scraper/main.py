import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://www.imdb.com/chart/top'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Failed to fetch page:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Newer, more reliable selectors
movies = soup.select('a.ipc-title-link-wrapper')  # main title links
ratings = soup.select('span.ipc-rating-star')  # ratings with score
# Votes are often in the same rating element or nearby

data_list = []

for i, link_tag in enumerate(movies[:250], 1):  # safety limit
    # Title and link
    title = link_tag.get_text(strip=True)
    href = link_tag.get('href')
    full_link = f"https://www.imdb.com{href}" if href and href.startswith('/') else href

    # Extract year from nearby text (often in a span like (1994) or metadata)
    year_match = re.search(r'\((\d{4})\)', link_tag.parent.get_text() if link_tag.parent else title)
    year = year_match.group(1) if year_match else "N/A"

    # Rating (e.g., 9.2)
    rating = "N/A"
    if i - 1 < len(ratings):
        rating_text = ratings[i - 1].get_text(strip=True)
        rating_match = re.search(r'(\d+\.\d+)', rating_text)
        if rating_match:
            rating = rating_match.group(1)

    # Crew / director (often in title attribute on the link or nearby)
    crew = link_tag.get('title') or "N/A"

    # Votes - harder now, often requires more complex parsing or is in aria-label
    votes = "N/A"

    data_list.append({
        "place": i,
        "movie_title": title,
        "year": year,
        "star_cast": crew,
        "rating": rating,
        "vote": votes,
        "link": full_link
    })

# Write to CSV (moved outside the loop!)
field_names = ['place', 'movie_title', 'year', 'star_cast', 'rating', 'vote', 'link']
with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data_list)

print(f"Successfully scraped {len(data_list)} movies and saved to movies.csv")
