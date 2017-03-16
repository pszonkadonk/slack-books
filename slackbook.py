import os
import time
from slackclient import SlackClient
from book import BookClient

class SlackBook:
    def __init__(self, bot_id, slack_client, watson_conversation, book_client):

        self.bot_id = bot_id
        self.slack_cleint = slack_client
        self.watson_conversation = watson_conversation
        self.book_client = book_client
        self.delay = 1
        self.workspace_id = 'c1a2722a-b334-4b16-a197-ec4e293d5fc9'

        self.bot_directed = "<@" + bot_id + ">"

    def format_book_info(self, book_description, book_rating):

        #do things

    def handle_selection_message(self, selection):
        book_id = self.context['books'][selection-1]['book_id']
        book_description = self.book_client.get_book_info_by_id(book_id)
        book_rating = self.context['books'][selection-1]['average_rating']

        return self.format_book_info(book_description, book_rating)


    def handle_message(self, message, channel):
        """
        Function is called whenever an individual directs a message at bot.
        If the message is valid, the bot will act on the message.  If it is not,
        the bot will respond make, asking the user to rephrase their request.
        """
        watson_response = self.watson_conversation.message(
            workspace_id = self.workspace_id
            message_input = {"text": message}
            context = self.context)

        self.context = watson_response["context"]

        if 'is_author' in self.context.keys() and self.context['is_author']:
            response = self.handle_author_message(message)

        elif 'is_selection' in self.context.keys() and self.context['is_selection']:
            response = "Invalid entry. Press any key to see your choices again"
            
            if self.context['selection'].isdigit():
                selection = int(self.context['selection'])
                if selection >= 1 and selection <= 20:
                    self.context['seletion_valid'] = True
                    response = self.handle_selection_message(selection)

        elif watson_response['entities'] and watson_response['entities'][0]['entity'] == 'genre':
            genre = watson_response['entities'][0]['value']
            response = self.handle_genre_message(genre)

        else:
            response = ''
            for text in watson_response['output']['text']:
                response += text + "\n"            
        
        self.respond_to_message(response, channel)

        

    def handle_author_message(self, message):
        if self.context['get_books']:
            self.context['books'] = self.book_client.find_by_author(message)

        response = "Ive found the following books for that author: \n"

        for i, book in enumerate(self.context['books']):
            response += str(i+1) + ". " + book['book_title'] + "\n"
        response+= "Please enter the number of the book you would like to know more about"

        return response


    def parse_output(self, slack_rtm_output):
        """
            This parsing function listens to all communcications 
            in the slack channel and returns None unless a message 
            is directed at the bot, based upon its ID
        """
        output = slack_rtm_output
        if output and len(output) > 0:
            for message in output:
                if message and 'text' in message and BOT_DIRECTED in message['text']:
                    return message['text'].split(BOT_DIRECTED)[1].strip().lower(), \
                        message['channel']
        return None, None
    
    def respond_to_message(self, response, channel):
        self.slack_client.api_call("chat.postMessage", channel = channel,
                                text = response, as_user = True)


    def run(self):
        DELAY = 1
        if slack_client.rtm_connect():
            print("slack-books-bot connected...")
            while True:
                command, channel = self.parse_output(self.slack_client.rtm_read())
                if(command and channel):
                    handle_message(command, channel)
                time.sleep(DELAY)
        else:
            print("Could not connect to slack.  Please check slack api token or bot id")


