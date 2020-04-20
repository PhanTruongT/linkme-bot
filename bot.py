import re
import praw
import json
import config
import logging
import requests

#BOT WILL BE ENTIRELY CONFIGURABLE THROUGH CONFIG.py


 #TODO reply to comment with link and add to postgres db
#reddit.comment(comment_id).reply('PLACEHOLDER')


def main():
    #Attempt login
    try:
        reddit = praw.Reddit(client_id=config.client_id,
                        client_secret=config.client_secret,
                        password=config.password,
                        user_agent=config.user_agent,
                        username=config.username)
    
    except:
        #TODO error handling
        pass

    #Iterate through newly submitted comments
    for comment_id in reddit.subreddit(config.subreddits).stream.comments(skip_existing=True):
        #Compile Regex
        
        comment_body = reddit.comment(comment_id).body
        #Check for the configured keyword 
        if comment_body.find(config.keyword):
            clean_body = sanitize_input(comment_body)
            
            #TODO search configured keyword through regex
            

            




#TODO Clean input of illegal characters
def sanitize_input(comment_body):
    #To lowercase
    comment_body = comment_body.lower()
    #
    return comment_body

if __name__ == "__main__":
    main()

    