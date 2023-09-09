from flask import Flask, jsonify
import praw 
import configparser
import os

app = Flask(__name__)

# Create a configparser instance and read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Reddit API credentials
client_id = os.environ.get('REDDIT_CLIENT_ID') #config['reddit']['client_id']
client_secret = os.environ.get('REDDIT_CLIENT_SECRET') #config['reddit']['client_secret']
user_agent = os.environ.get('REDDIT_USER_AGENT') #config['reddit']['user_agent']  # A unique user agent, e.g., "my_app_name by /u/your_username"

# Initialize the Reddit API
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

# Specify the subreddit you want to retrieve messages from
subreddit_name = 'bitcoin'


@app.route('/get_messages', methods=['GET'])
def get_messages():
    # Fetch the last 10 hot posts from the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    hot_posts = subreddit.hot(limit=10)

    messages = []

    for i, post in enumerate(hot_posts):
        # Get the top comment with the most upvotes
        top_comment = None
        top_score = -1

        post.comments.replace_more(limit=0)  # Ensure all comments are loaded

        for comment in post.comments:
            if comment.score > top_score:
                top_score = comment.score
                top_comment = comment

        if top_comment:
            message = {
                "title": post.title,
                "top_comment": top_comment.body
            }
        else:
            message = {
                "title": post.title,
                "top_comment": None
            }

        messages.append(message)

    return jsonify(messages)


if __name__ == '__main__':
    app.run(debug=True)
