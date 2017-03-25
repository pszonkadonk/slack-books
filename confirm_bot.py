import os
from slackclient import SlackClient


"""
Makes a call to Slack API to confirm that the 
bot we want to communicate with exists in Slack
"""


BOT_NAME = 'slack-books-bot'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


if __name__ == '__main__':
    api_call_users = slack_client.api_call("users.list")
    if api_call_users.get("ok"):
        users = api_call_users.get("members")
        for user in users:
            if "name" in user and user.get("name") == BOT_NAME:
                print("BOT ID for " + user["name"] + " is " + user.get("id"))
            else:
                print("There is no bot user with the name " + BOT_NAME)