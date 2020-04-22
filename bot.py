import re
import praw
import json
import config
import logging
import requests

# BOT WILL BE ENTIRELY CONFIGURABLE THROUGH CONFIG.py


# TODO reply to comment with link and add to postgres db
# reddit.comment(comment_id).reply('PLACEHOLDER')


def main():
    # Attempt login
    try:
        reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            password=config.password,
            user_agent=config.user_agent,
            username=config.username,
        )

    except:
        # TODO error handling
        pass

    # Iterate through newly submitted comments
    for comment_id in reddit.subreddit(config.subreddits).stream.comments(
        skip_existing=True
    ):
        comment_body = reddit.comment(comment_id).body

        # Check for the configured keyword
        if comment_body.find(config.keyword):
            clean_comment = sanitize_input(comment_body)

            #Any non alphanumeric or
            pattern = r"\W!linkme \w\w|^!linkme\w\w"
            compiled_keyword_regex = re.compile(pattern, re.I | re.M)

            keyword_indices = []
            for m in compiled_keyword_regex.finditer(clean_comment):
                keyword_indices.append(m.start())
                print(m.start())
            # Extract search keys
            search_keys = []
            for index_i, key_i in enumerate(keyword_indices):
                begin = index_i + 7

                # On last keyword, set end to the end of the string
                if index_i == len(keyword_indices) - 1:
                    end = len(clean_comment)

                # Set end to end of line, or the starting index of next command keyword
                else:
                    # check for index of next nextline #TODO FIX, NOT DETECTING NEWLINE
                    for body_index, element in enumerate(
                        comment_body[index_i : len(clean_comment)]
                    ):
                        if element == "\n":
                            next_newline = body_index

                    next_key = keyword_indices[index_i + 1]
                    print("next index", keyword_indices[index_i + 1])
                    if next_newline > keyword_indices[index_i + 1]:
                        end = next_key
                    else:
                        end = next_newline

                local_search_keys = clean_comment[begin:end]
                for key in local_search_keys:
                    search_keys.append(key)

            for i in search_keys:
                print(i)


# TODO Clean input of illegal characters
def sanitize_input(comment_body):
    clean_comment = comment_body
    return clean_comment


if __name__ == "__main__":
    main()
