import re
import praw
import json
import config
import logging
import requests

# BOT WILL BE ENTIRELY CONFIGURABLE THROUGH CONFIG.py

#TODO LOGGING, REPLACE ALL PRINTS
#TODO Fix get_search_keys()


# TODO reply to comment with link and add to postgres db
# TODO break refactor debug into functions
# TODO unittest


def main():
    reddit = login()
    
    # Iterate through newly submitted comments
    for comment_id in reddit.subreddit(config.subreddits).stream.comments(
        skip_existing=True
       
    ):
        
        clean_comment = get_clean_comment(reddit.comment(comment_id).body)

        # Check for keyword in comment
        if clean_comment.find(config.keyword):
            get_search_keys(clean_comment)
       
    


# Extract a list of search keys
def get_search_keys(clean_comment):
        keyword_indices = get_keywords_pos(clean_comment)

        search_keys = []
        for index_i, key_i in enumerate(keyword_indices):
            begin = key_i + 8
            print('begin', begin, 'current index', index_i)
            # On last keyword, set end to the end of the string 
            if index_i == len(keyword_indices) - 1:
                end = len(clean_comment)

            # Set end to end of line, or the starting index of next command keyword
            else:
                # Check for index of next nextline #TODO FIX, NOT DETECTING NEWLINE
                # Replace index_i with key_i  replace body index with key_i + body_index
                for body_index, element in enumerate(
                    clean_comment[index_i : len(clean_comment)]
                ):
                    if element == '\n':
                        next_newline = body_index
                        #break needed

                next_key = keyword_indices[index_i + 1]
                print("next index", keyword_indices[index_i + 1])
                if next_newline > keyword_indices[index_i + 1]:
                    end = next_key
                else:
                    end = next_newline

            local_search_keys = clean_comment[begin:end]
            for key in local_search_keys.split():
                search_keys.append(key)
        
        print(search_keys)




def login():
    # Attempt login
    try:
        reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            password=config.password,
            user_agent=config.user_agent,
            username=config.username,
        )

    # TODO error handling
    except:
        pass

    return reddit


    
# TODO Clean input of illegal characters
def get_clean_comment(comment):
    clean_comment = comment
    return clean_comment



# Get starting position of all keyword matches
def get_keywords_pos(clean_comment):
    pattern = r"\W!linkme \w\w|^!linkme \w\w"
    compiled_keyword_regex = re.compile(pattern, re.I | re.M)

    keyword_indices = []
    for m in compiled_keyword_regex.finditer(clean_comment):

        # If match is not at the start of the comment
        if(m.start != 0):
            #Add 1 to starting position of match to skip over a space character
            keyword_indices.append(m.start()+1)
        else:
            keyword_indices.append(m.start())

    return keyword_indices




if __name__ == "__main__":
    main()
