import os
import time
from slackclient import SlackClient

class SlackBook:
    def __init__(self, bot_id, slack_client, watson_conversation, goodreads_client):

        self.bot_id = bot_id
        self.slack_cleint = slack_client
        self.watson_conversation = watson_conversation
        self.goodreads_client = goodreads_client
        self.delay = 1
        self.workspace_id = 'c1a2722a-b334-4b16-a197-ec4e293d5fc9'

        self.bot_directed = "<@" + bot_id + ">"

    def handle_message(self, command, channel):
        """
        Function is called whenever an individual directs a message at bot.
        If the command is valid, the bot will act on the command.  If it is not,
        the bot will respond make, asking the user to rephrase their request.
        """
        watson_response = self.watson_conversation.message(
            workspace_id = self.workspace_id
            message_input = {"text": command}
            context = self.context)
            
        response = "Sorry, I'm not sure what you are asking for.  Please rephrase your question."

        if(command.startswith(EXAMPLE_COMMAND)):
            response = "sure write some more and I can do that"
        
        self.respond_to_message(response, channel)


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

