
import praw
import logging
import config

import requests
import json

#TODO get logger


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

    #iterate through newly submitted comments
    for comment_id in reddit.subreddit(config.subreddits).stream.comments(skip_existing=True):
        
        #Search for keyword (with valid spacing)
        if reddit.comment(comment_id).body.find(config.keyword + ' ',0,6):
            #TODO reply to comment with link and add to postgres db
            print('command received')
            reddit.comment(comment_id).reply('PLACEHOLDER')
            
        


    

if __name__ == "__main__":
    main()

    