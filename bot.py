import re
import praw
import json
import config
import logging
import requests
import utils

# BOT WILL BE ENTIRELY CONFIGURABLE THROUGH CONFIG.py

# TODO unittest
# TODO type checking


# TODO reply to comment with link and add to postgres db
# TODO break refactor debug into functions


logger = utils.make_logger(config.logfile, config.logLevel)

def main():
    reddit = login()

    # Iterate through newly submitted comments
    for comment_id in reddit.subreddit(config.subreddits).stream.comments(
        skip_existing=True
    ):
        clean_comment = get_clean_comment(reddit.comment(comment_id).body)
        logger.info(f'Clean comment: \n {clean_comment}')

        # Check for keyword in comment
        if clean_comment.find(config.keyword) != -1:
            logger.info('Keyword Found')

            keyword_list = get_search_keys(clean_comment)
            logger.info(keyword_list)


# Extract a list of search keys
def get_search_keys(clean_comment):
    keyword_indices = get_keywords_pos(clean_comment)

    keyword_list = []
    # Find starting and ending pos
    for list_i, comment_i in enumerate(keyword_indices):

        begin = comment_i + len(config.keyword)

        # On last keyword, set end to the end of the comment
        if list_i == len(keyword_indices) - 1:
            end = len(clean_comment)

        # Set end to the next keyword, or next newline
        else:
            next_keyword = keyword_indices[list_i + 1]
            next_newline = get_next_newline(comment_i, clean_comment)

            # Set end to whichever is closest next_newline or next_keyword
            if next_newline is not None:
                if next_newline > next_keyword:
                    end = next_keyword
                elif next_newline < next_keyword:
                    end = next_newline
                else:
                    logger.warning('IMPOSSIBLE :: next_newline == next_keyword ')
            else:
                logger.info("There are no next newline")
                end = next_keyword

        local_keywords_string = clean_comment[begin:end]
        local_keywords_list = re.split(r",", local_keywords_string)

        local_keywords_list = map(str.strip, local_keywords_list)
        keyword_list.extend(local_keywords_list)
    return keyword_list


def login():
    logger.info('Attempting login')
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
    clean_comment = comment.strip()
    return clean_comment


# Get starting position of all keyword matches
def get_keywords_pos(clean_comment):
    pattern = r"\W!linkme \w\w|^!linkme \w\w"
    compiled_keyword_regex = re.compile(pattern, re.I | re.M)

    keyword_indices = []
    for m in compiled_keyword_regex.finditer(clean_comment):

        # If match is not at the start of the comment
        if m.start != 0:
            # Add 1 to starting position of match to skip over a space character
            keyword_indices.append(m.start() + 1)
        else:
            keyword_indices.append(m.start())

    return keyword_indices


# Returns index of next newline, returns None if there are no newlines
def get_next_newline(comment_i, clean_comment):
    clean_comment_sub = clean_comment[comment_i:]
    next_newline = None

    # Iterate through comment substring, find index of next newline
    for char_count, char in enumerate(clean_comment_sub):
        if char == "\n":
            next_newline = comment_i + char_count
            break

    return next_newline


if __name__ == "__main__":
    main()
