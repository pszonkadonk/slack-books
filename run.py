import os
import json
import time
from dotenv import load_dotenv
from slackclient import SlackClient
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features

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

  natural_language_understanding = NaturalLanguageUnderstandingV1(
    username = os.environ.get("NATURAL_LANGUAGE_UNDERSTANDING_USERNAME"),
    password = os.environ.get("NATURAL_LANGUAGE_UNDERSTANDING_PASSWORD"),
    version= "2017-02-27" 
  )

  book_client = BookClient(os.environ.get("GOODREADS_API"))

  slack_books_bot = SlackBook(bot_id, 
                      slack_client, 
                      conversation_agent,
                      natural_language_understanding,
                      features,
                      book_client)
                      
  slack_books_bot.run()