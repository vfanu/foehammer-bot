from slackclient import SlackClient
import os

# Bot user (malbot_test)
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

def init_connection():
    return slack_client.rtm_connect(with_team_state=False)


def get_bot_id():
    return '<@' + slack_client.api_call("auth.test")["user_id"] + '>'


def send_message(channel, message):
    print('sending message ', message)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )


def read_message():
    return slack_client.rtm_read()


def auth_client():
    slack_client.api_call("auth.test")
