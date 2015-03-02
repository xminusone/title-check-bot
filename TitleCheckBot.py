import praw
import time
import urllib.request
from bs4 import BeautifulSoup


# Reddit account
username = "bot_username"
password = "bot_password"

# Submission Limit (max submissions checked - for testing purposes)
# Change "1000" to whatever you'd like the limit to be. (1000 is PRAW's max submissions it will pull)
thing_limit = 100

# Startup stuff
print('Title Check Bot')
print('Waiting for Windows to start...') # I have the bot run at boot, if you don't want this extra wait time, comment out the next line.
time.sleep(5)
print('Reticulating splines...')
time.sleep(3)

# Reddit login and user agent
reddit = praw.Reddit(user_agent="Title Check Bot v0.2 (your username here)")
print('Logging in to Reddit...')
reddit.login(username, password)
print('Logged in successfully.  Checking for unmoderated items...')

# Subreddit being monitored (you should use "mod" if you want to check all subreddits the bot mods)
subreddit = reddit.get_subreddit("mod")

# Grabs Article Text
def URLisValid(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False
def getArticleText(url):
    if URLisValid(url):
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page)
        return str(soup)

# Reddit Stuff
for submission in subreddit.get_unmoderated(limit=thing_limit):
    title = submission.title
    articletext = getArticleText(submission.url)
    if articletext is not None:
        if title.lower() in articletext.lower():
            print('Submission has correct title. Ignored. Moving on...')
        else:
            print('Submission has wrong title.  Waiting 10 seconds for AutoModerator to check...')
            time.sleep(10)  # Keeps Title Check Bot from removing submissions that AutoMod would have removed anyway.
            submission.add_comment("Removed. Please see the sidebar for our rules.").distinguish()
            submission.remove()
            print('Submission removed. Moving on...')
