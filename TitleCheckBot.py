import praw
import time
import requests

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
print('Reticulating splines...')
time.sleep(3)
reddit = praw.Reddit(user_agent="FILL THIS IN")
print('Logging in to Reddit...')
reddit.login(username=username, password=password)
print('Logged in successfully.  Checking for unmoderated items...')

# Title Checker
stream = praw.helpers.submission_stream(reddit, subreddit, limit=thing_limit)
for submission in stream:
    title = submission.title
    article = requests.get(submission.url)
    if submission.approved_by:
        print('Submission already approved. Ignored. Moving on...')
        continue
    if title.lower() in article.text.lower():
        print('Submission has correct title. Ignored. Moving on...')
    if title.lower() not in article.text.lower():
        print('Submission has wrong title.  Waiting 10 seconds for AutoModerator to check...')
        time.sleep(10) # Keeps Title Check Bot from removing submissions that AutoMod would have removed anyway.
        submission.add_comment("REMOVAL COMMENT GOES HERE").distinguish()
        submission.remove()
        print('Submission removed. Moving on...')
