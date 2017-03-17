import os
import time
from dotenv import load_dotenv
from slackclient import SlackClient
from watson_developer_cloud import ConversationV1

from book import BookClient
from slackbook import SlackBook

if __name__ == "__main__":
  load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

  bot_id = os.environ.get("BOT_ID")

  slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

  conversation_agent = ConversationV1(
    username=os.environ.get("CONVERSATION_USERNAME"),
    password=os.environ.get("CONVERSATION_PASSWORD"),
    version= "2017-02-03"
    )

  book_client = BookClient(os.environ.get("GOODREADS_API"))

  slack_books_bot = SlackBook(bot_id, 
                      slack_client, 
                      conversation_agent,
                      book_client)
                      
  slack_books_bot.run()