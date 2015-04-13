import praw
import time
import urllib.request
import warnings
import sys
from bs4 import BeautifulSoup
 
# Supresses warnings in console- BeautifulSoup generates some annoying depreciation warnings we can't avoid
warnings.filterwarnings("ignore")
 
# Reddit account login infp
username = "YOUR_BOT_USERNAME"
password = "YOUR_BOT_PASSWORD"
 
# Submission Limit (max newest submissions that will be checked)
# Change this to whatever you'd like the limit to be. (1000 is PRAW's max submissions it will pull)
# Setting this to a low number will avoid removals due to titles changed after submission.
thing_limit = 10
 
# Startup stuff
print('Title Check Bot is Starting Up - v1.1de')
print('     ')
print('Waiting for Windows to start...') # I have the bot run at boot, if you don't want this extra wait time, comment out the next few lines.
time.sleep(5)
print('Reached fhqwhgads limit! ert+ y76p -lu8jykee;Strong ba15456----++++gf')
time.sleep(5)
 
# Imports domain exemption list
print('Importing the domain exemption list from exemptions.cfg...')
try:
    with open('exemptions.cfg', 'r') as f:
          exemptlist = [line.strip() for line in f]
    print('Done!')
except:
    print('Error! exemptions.cfg is missing. This may cause submissions to be incorrectly removed.') 
 
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
            print('Error!  removalcomment.cfg is missing. Attempts to post removal comments may fail...')
            pass
    except IOError:
        print('Error!  removalcomment.cfg is missing. Attempts to post removal comments may fail...')
        pass
    except:
        print('Error!  removalcomment.cfg is missing or something bad happened. Attempts to post removal comments may fail...')
        pass
    return comment
print('Done!')
 
# Reddit login and user agent
reddit = praw.Reddit(user_agent="Title Check Bot v1.1de - /u/YOUR_USERNAME_HERE")
print('Logging in to Reddit...')
try:
    reddit.login(username, password)
except:
    print("Login failed!  Can't complete startup.  Is Reddit down?  Is your username/pasword incorrect?")
    time.sleep(10)
    sys.exit(0)
print("Logged in successfully. Startup tasks complete.")
print('     ')
print('----------')
print("Checking unmoderated queue for /r/mod...")
 
# Subreddit being monitored (you probably want /r/mod so all modded subs will be checked)
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
        try:
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
                    time.sleep(5)  # Keeps Title Check Bot from removing submissions that AutoMod would have removed anyway. Don't need this if you are using the new integrated AutoMod.
                    submission.remove()
                    submission.set_flair(flair_text='Wrong/Altered Title- Removed', flair_css_class='removed')
                    print('Flair set! Posting removal comment... (', submission.author.name, ')')
                    submission.add_comment(getRemovalComment()).distinguish()
                    print('Removed submission. (', submission.author.name, ')')
        except:
            print('I AM ERROR. Reddit gave us an API error or something, skipping this submission...')
            pass
while True:
        try:
            titleCheck()
            #print('----------')
            print('Checked all unmoderated items. Rechecking in 2 minutes...')
            time.sleep(60)
            print('Rechecking in 1 minute...')
            time.sleep(60)
            print('----------')
            print('Checking for unmoderated items.')
        except:
            print('THANKS OBAMA!  Reddit gave an error or a submission was deleted.  Skipping and will retry next cycle...')
            time.sleep(60)
            pass
