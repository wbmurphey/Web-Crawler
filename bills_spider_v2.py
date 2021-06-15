#!/usr/bin/env python3

#Web Spider by Bill Murphey
#Written for SecureSet's Networks 400 class
#4/6/2021


#Importing the regular expressions and requests libraries
import re
import requests

#The user is prompted to enter a website
usr_input = input("Enter a website: https:// ")

#user is asked how many URLs are scraped before the spider will stop crawling
max_links = int(input("Enter number of URLs to visit before stopping: "))

#the spider gets the webpage entered (prepended with https:// for convienence) and assigns it to a variable
home_page = requests.get(f"https://{usr_input}")

#defining a regular expression to use to find URLs in the webpage
url_regex = '(https?:\/\/.+?(?=["]))'

#using the defined regular expression to pull out all URLs matching the template into a variable in a list format
scraped_urls = re.findall(url_regex, home_page.text)

#defining an empty list to keep track of links the spider already visited
links_visited = []

#A running total of how many URLs were discovered, but not necessarily visited
url_count = len(scraped_urls)
"""
This is the meat and potatoes of the spider
The program will iterate through all of the links stored in the list we established above
It will check if each link is already in the list of previously visited links
It will also check if the maximum number of links visited has been reached
If neither of these conditions have been met, the code gets the webpage at each link, appends it to the list of visited links
It will handle errors caused by scraped URLs that the requests library doesn't understand
Now that the link has been determined to be valid, the spider scrapes URLs from that link
The new URLs are added to the list of unvisited URLs
The spider displays a message to the users about how many URLs were found on each link
"""
for link in scraped_urls:
    if link not in links_visited and len(links_visited) < max_links:
        try:
            page = requests.get(link)
            print(f"Visiting {link}...")
            links_visited.append(link)
        except:
            print(f"{link} could not be visited. {link} is likely not a valid URL.")
            pass
        if link in links_visited:
            new_scraped_urls = re.findall(url_regex, page.text)
            scraped_urls.extend(new_scraped_urls)
            url_count += len(new_scraped_urls)
            print(f"The spider found {len(new_scraped_urls)} URLs in {link}\n")

#Here the spider summarizes the URLs that it visited
print(f"\n\nThe spider discovered a total of {url_count} URLs within https://{usr_input}\nThe spider visited the following URLs (with a maximum of {max_links}):\n")
for i in links_visited:
    print(i)
