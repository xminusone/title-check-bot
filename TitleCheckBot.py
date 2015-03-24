import praw
import time
import urllib.request
import warnings
from bs4 import BeautifulSoup

# Supresses warnings in console that BeautifulSoup triggers
warnings.filterwarnings("ignore")

# Reddit account
username = "Your_Bot_Username"
password = "Your_Bot_Password"

# Submission Limit (max submissions checked - for testing purposes)
# Change "1000" to whatever you'd like the limit to be. (1000 is PRAW's max submissions it will pull)
thing_limit = 1000

# Startup stuff
print('Title Check Bot is Starting Up - v1.0r')
print('     ')
print('Waiting for Windows to start...') # I have the bot run at boot, if you don't want this extra wait time, comment out the next line.
time.sleep(10)
print('Loading fhqwhgads module...')
time.sleep(5)

# Imports domain exemption list
print('Importing the domain exemption list from exemptions.cfg...')
with open('exemptions.cfg', 'r') as f:
          exemptlist = [line.strip() for line in f]
time.sleep(2)
print('Done!')
time.sleep(1)

# Imports removal comment
print('Importing the removal comment from removalcomment.cfg...')
import os
def getRemovalComment():
    comment = ''
    try:
        if not os.path.exists('removalcomment.cfg'):
            raise IOError
        with open('removalcomment.cfg') as file:
            for line in file:
                comment += line
        try:
            file.close()
        except:
            pass
    except IOError:
        pass
    except:
        pass
    return comment
print('Done!')

# Reddit login and user agent
reddit = praw.Reddit(user_agent="Title Check Bot v1.0r - /u/YOUR_USERNAME")
print('Logging in to Reddit...')
reddit.login(username, password)
print("Logged in successfully. Startup tasks complete.")
print('     ')
print('----------')
print("Checking unmoderated queue for /r/mod...")

# Subreddit being monitored (you should use "mod" if you want to check all subreddits the bot mods)
subreddit = reddit.get_subreddit("mod")

# Grabs Article Text
def URLisValid(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        print('Flagrant System Error! URL failed to load. Cannot check this submission.')
        return False
def getArticleText(url):
    if URLisValid(url):
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page)
        return str(soup)

# Reddit Stuff
def titleCheck():
    for submission in subreddit.get_unmoderated(limit=thing_limit):
        title = submission.title
        articletext = getArticleText(submission.url)
        exemptcheckurl = submission.url
        if articletext is not None:
            # Check against domain exemption list
            if any(domain in exemptcheckurl for domain in exemptlist):
                print('Domain is on exemption list. Cannot check this submission. (', submission.author.name, ')')
            # Check if title is in article
            elif title.lower() in articletext.lower():
                print('Submission has the correct title. (', submission.author.name, ')')
            # Reports for submissions, with wrong titles, that are at greater than +50
            elif submission.score > 50:
                print('Submission has wrong title, but has more than 50 upvotes. Reporting...')
                submission.report(reason='Submission may have wrong title, but is at +50. v1.0b_de')
                print('Reported submission. (', submission.author.name, ')')
            # Reports for submissions that have the wrong title
            else:
                print('Submission has wrong title.  Waiting 5 seconds for AutoModerator to check...')
                time.sleep(5)  # Keeps Title Check Bot from removing submissions that AutoMod would have removed anyway.
                submission.remove()
                print('Posting removal comment... (', submission.author.name, ')')
                submission.add_comment(getRemovalComment()).distinguish()
                print('Removed submission. (', submission.author.name, ')')
while True:
        titleCheck()
        #print('----------')
        print('Checked all unmoderated items. Rechecking in 5 minutes...')
        time.sleep(240)
        print('Rechecking in 1 minute...')
        time.sleep(60)
        print('----------')
        print('Checking for unmoderated items.')

