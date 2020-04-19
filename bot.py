import time
import praw
import config

#(config.client_id, config.client_secret,
#                    config.password, config.user_agent,
#                   config.username)


user_agent = "Karma breakdown 1.0 by /u/_Daimon_"
r = praw.Reddit(user_agent=user_agent)
r.login(config.username,config.password)