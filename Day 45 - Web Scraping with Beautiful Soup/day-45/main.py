from bs4 import BeautifulSoup
import requests
import lxml

# with open("website.html") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, "html.parser")
# soup = BeautifulSoup(contents, 'lxml')      #functions the same as the above line, but uses lxml in the case the "html.parser" does not work for a site
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)

# print(soup.prettify())

# print(soup.a)       #returns the first <a> tag (anchor tag)
# print(soup.li)      #returns the first <li> tag (list tag)
# print(soup.p)       #returns the first <p> tag (paragraph tag)

# all_anchor_tags = soup.find_all(name="a")       # returns all <a> tags
# # print(all_anchor_tags)
# #
# # for tag in all_anchor_tags:
# #     # print(tag.getText())
# #     print(tag.get("href"))      # returns the link ("href") from an anchor tag
#
# heading = soup.find(name="h1", id="name")       # returns the first instance of an <h1> tag with the id "name"
# print(heading)
#
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.getText())
#
# # company_url = soup.select_one(selector="p a")       # returns the first instance where an anchor tag lies in a paragraph tag
# # print(company_url)
#
# name = soup.select_one(selector="#name")            # returns the first instance where an id of "name" shows up
# print(name)
#
# headings = soup.select(".heading")              #returns the first instance where a class with type "heading" shows up
# print(headings)

response = requests.get("https://appbrewery.github.io/news.ycombinator.com/")
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")

articles = soup.find_all(name="a", class_="storylink")
print(articles)
article_texts = []
article_links = []
for articles in articles:
    text = articles.getText()
    article_texts.append(text)
    link = articles.get("href")
    article_links.append(link)
article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(article_texts[largest_index])
print(article_links[largest_index])

# print(article_texts)
# print(article_links)
# print(article_upvotes)
