#Using github sourced twitter ids for covid 19 data we cloned the repository and cleaned and then checked the urls of the twitter ids. 
#Then using chatGPT we did a sentiment analysis and then graphed the results after putting them in a dictionary.

#A scalable script that asks ChatGPT to take in different tweets in monthly categorized separated folders, 
#classify them by some metric, and then plot the data in a way that works best for your needs.

import openai
import pandas as pd
import numpy as np
import glob
import os
from IPython.display import HTML
import requests
import matplotlib.pyplot as plt 

counter = 0
openai.api_key = "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"

def show_tweet(link):
    '''Display the contents of a tweet. '''
    '''Returns Dani if error, else returns tweet'''
    url = 'https://publish.twitter.com/oembed?url=%s' % link
    response = requests.get(url)
    status = str(response.status_code).strip()
    if status != "200" and status != "201" and status != "202" and status != "203":
        return "Dani"
    else:
        html = response.json()["html"]
        return (html.split("blockquote")[1])

mydict = {}
os.chdir(r'C:/Users/Leo/Documents/test/COVID-19-TweetIDs')
my_folders = glob.glob('*')
for folder in my_folders:
    os.chdir(r'C:/Users/Leo/Documents/test/COVID-19-TweetIDs' + '/' + folder)
    txt_files = glob.glob('*.txt')
    for txt_file in txt_files:
        formatted_date = txt_file[26:-7]
        mytext = open('C:/Users/Leo/Documents/test/COVID-19-TweetIDs' + '/' + folder + '/' + txt_file)
        data = mytext.read().split("\n") 
        running_total = 0
        for id in data:
            counter += 1
            print(counter)
            tweet_link = "https://twitter.com/dani/status/" + id
            query = show_tweet(tweet_link)
            if query == "Dani":
                continue
            prompt = "Determine if this quote is negative or positive: \n" + "\""  + query + "\"\n" + "On a scale of -100 to 100 respond only with the number you would say best represents this tweet. I repeat your response should only consist of that number no other text."
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=2)
            running_total += int(chat_completion.choices[0].message.content)
            #print(running_total)
        avg = running_total/(len(data))
        mydict[formatted_date] = avg
        mytext.close()

print(mydict)

#SCATTER PLOT SCRIPT
lists = sorted(mydict.items())
x, y = zip(*lists)
plt.scatter(x, y)
plt.xlabel('Dates')
plt.ylabel('Scores')
plt.title('Sentiment Analysis of Twitter COVID Data')
plt.show()

#BAR PLOT SCRIPT
#names = list(mydict.keys())
#values = list(mydict.values())
#plt.bar(range(len(mydict)), values, tick_label=names)
#plt.show()











