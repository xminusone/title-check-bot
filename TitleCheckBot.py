import praw
import time
import requests
import urllib.request
from bs4 import BeautifulSoup

# Subreddit being monitored (you should use "mod" if you want to check all subreddits the bot mods)
subreddit = "mod"

# Reddit account
username = "BOT_USERNAME"
password = "BOT_PASSWORD"

# Submission Limit (max submissions checked - for testing purposes)
# Change "1000" to whatever you'd like the limit to be. (1000 is PRAW's max submissions it will pull)
thing_limit = 1000

# Startup stuff
print('Title Check Bot - Alpha')
print('Waiting for Windows to start...') # I have the bot run at boot, if you don't want this extra wait time, comment out the next line.
time.sleep(2)
print('Adjusting bell curves...')
time.sleep(10)
print('Decomposing singular values...')
time.sleep(10)
print('Reticulating splines...')
time.sleep(10)

# Reddit login and user agent
reddit = praw.Reddit(user_agent="Title Check Bot Alpha (run by YOUR USERNAME GOES HERE)")
print('Logging in to Reddit...')
reddit.login(username=username, password=password)
print('Logged in to Reddit successfully.  Checking for unmoderated items...')

# Grabs Article Text
def getArticleText(url):
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page)
    return str(soup)
    
# Reddit Stuff
for submission in subreddit.get_unmoderated(limit=thing_limit):
    title = submission.title
    articletext = getArticleText(submission.url)
    if title.lower() in articletext.lower():
        print('Submission has correct title. Ignored. Moving on...')
    else title.lower() not in articletext.lower():
        print('Submission has wrong title.  Waiting 10 seconds for AutoModerator...')
        time.sleep(10) # Keeps Title Check Bot from removing submissions that AutoMod would have removed anyway.
        submission.add_comment("REMOVAL COMMENT GOES HERE").distinguish()
        submission.remove()
        print('Submission removed. Moving on...')
