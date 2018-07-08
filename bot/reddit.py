"""This module uses PRAW to post the message to the desired post id."""

import praw

import config


def update_post(message):
    """Updates the Reddit post.

    Parameters
    ----------
    message : str
        The Markdown message to be posted.

    """

    # We initialize Reddit.
    reddit = praw.Reddit(client_id=config.APP_ID, client_secret=config.APP_SECRET,
                         user_agent=config.USER_AGENT, username=config.REDDIT_USERNAME,
                         password=config.REDDIT_PASSWORD)

    # We update the Reddit post.
    reddit.submission(config.SUBMISSION_ID).edit(message)
