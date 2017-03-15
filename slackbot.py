import os
import time
from slackclient import SlackClient


BOT_ID = os.environ.get('BOT_ID')

BOT_DIRECTED = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"


slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_mesage(command, channel):
    """
    Function is called whenever an individual directs a message at bot.
    If the command is valid, the bot will act on the command.  If it is not,
    the bot will respond make, asking the user to rephrase their request.
    """
    response = "Sorry, I'm not sure what you are asking for.  Please rephrase your question."

    if(command.startswith(EXAMPLE_COMMAND)):
        response = "sure write some more and I can do that"

    slack_client.api_call("chat.postMessage", channel = channel,
                          text = respone, as_user = True)

def parse_output(slack_rtm_output):
    """
        This parsing function listens to all communcications 
        in the slack channel and returns None unless a message 
        is directed at the bot, based upon its ID
    """
    output = slack_rtm_output
    if output and len(output) > 0:
        for message in output:
            if message and "text" in message and BOT_DIRECTED in message["text"]:
                return message["text"].split(BOT_DIRECTED)[1].strip().lower(),
                message["channel"]
    return None, None

    

if __name__ == "__main__":
    DELAY = 1
    if slack_client.rtm_connect():
        print("SlackBook bot connected.")
        while True:
            command, channel = parse_output(slack_client.rtm_read())
            if(command and channel):
                handle_message(command, channel)
            time.sleep(DELAY)
    else:
        print("Could not connect to slack.  Please check slack api token or bot id")

