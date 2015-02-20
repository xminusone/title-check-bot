import praw
import requests

# Subreddit being monitored (you should use "mod" to just check all subreddits the bot mods)
subreddit = "mod"

# Reddit account
username = "BOT_USERNAME"
password = "BOT_PASSWORD"

# Bot Stuff
reddit = praw.Reddit(user_agent="Fill This In")
print('Logging in to Reddit...')
reddit.login(username=username, password=password)
print('Logged in.  Checking /r/mod for unmoderated items...')

stream = praw.helpers.submission_stream(reddit, subreddit)
for submission in stream:
    title = submission.title
    article = requests.get(submission.url)
    if submission.approved_by:
        print('Already approved. Moving on...')
        continue
    if title.lower() in article.text.lower():
        print('Correct title. Moving on...')
    if title.lower() not in article.text.lower():
        submission.add_comment("Removal Comment Goes Here").distinguish()
        submission.remove()
        print('Submission removed, wrong title. Moving on...')
