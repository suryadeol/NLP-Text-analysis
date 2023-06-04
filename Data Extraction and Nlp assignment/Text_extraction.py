#!/usr/bin/env python
# coding: utf-8

# # Extracting data from the web page with given url link and saving it into text file with url_id as its file name

# In[ ]:


import requests
from bs4 import BeautifulSoup
from pandas import *


# # Making obsered tags and classes into if-else cases and ran a single loop to get all text files

# In[ ]:


def convert_to_text_file(uid,url):
    # Make a request to the website
    #url = "https://insights.blackcoffer.com/ai-in-healthcare-to-improve-patient-outcomes/"
    response = requests.get(url)

    # Parse the HTML content of the website
    soup = BeautifulSoup(response.content, 'html.parser')

    if(soup.find('h1', {'class': 'entry-title'})!=None):
        
        # Extract the article title
        title = soup.find('h1', {'class': 'entry-title'}).text.strip()


        # Extract the article text
        article = ''
        for paragraph in soup.find_all('div', {'class': 'td-post-content'}):
            article += paragraph.text.strip()


        # Write the title and article to a text file
        with open(str(uid)+".txt", 'w',  encoding='utf-8') as f:
            f.write(title + '\n\n')
            f.write(article)

        # Print a confirmation message
        print('Article saved to file!')
    
    elif(soup.find('h1', {'class': 'tdb-title-text'})!=None):
        
        # Extract the article title
        title = soup.find('h1', {'class': 'tdb-title-text'}).text.strip()


        # Extract the article text
        article = ''
        for paragraph in soup.find_all('div', {'class': 'td-post-content'}):
            article += paragraph.text.strip()


        # Write the title and article to a text file
        with open(str(uid)+".txt", 'w',  encoding='utf-8') as f:
            f.write(title + '\n\n')
            f.write(article)

        # Print a confirmation message
        print('Article saved to file!')
        
    else:
        # Extract the article title
        title = soup.find('h3', {'class': 'tdm-title tdm-title-md'}).text.strip()


        # Extract the article text
        article = ''
        for paragraph in soup.find_all('div', {'class': 'td-post-content'}):
            article += paragraph.text.strip()


        # Write the title and article to a text file
        with open(str(uid)+".txt", 'w',  encoding='utf-8') as f:
            f.write(title + '\n\n')
            f.write(article)

        # Print a confirmation message
        print('Article saved to file!')
        
        


# In[ ]:


df=read_csv('Input.xlsx - Sheet1.csv')

url_id=df.iloc[:,0]
url_link=df.iloc[:,1]

for i in range(2,len(df)):
    convert_to_text_file(url_id[i],url_link[i])
    


# In[ ]:





# In[ ]:




