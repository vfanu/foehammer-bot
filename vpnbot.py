import time
import re
import response_generator
import slack_messenger
import os
import aws_region_finder
from subprocess import Popen

mention_regex = "@FoeHammer"

RTM_READ_DELAY = 1
COMMANDS = {"start vpn": "start vpn",
            "stop vpn": "stop vpn",
            "whats going on?": "get info",
            "hi": "send greetings"}


def parse_bot_message(slack_events, vpnbot_id):

    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == vpnbot_id:

                return_message = ''
                index = 1
                while index < len(message):
                    if index == 1:
                        return_message = message[index]
                    else:
                        return_message += ' ' + message[index]
                    index += 1

                    if return_message in COMMANDS:
                        return event["channel"], str.strip(return_message), message

                return event["channel"], str.strip(return_message)

    return None, None, None


def parse_direct_mention(message_text):
    print(mention_regex)
    print(message_text)
    matches = re.search(mention_regex, message_text)

    if (matches is not None and matches.group(0) is not None):
        message = str.split(str(message_text))
        return message[0], message

    else:
        return None, None


def start_vpn(region, email):
    print('Starting a new VPN instance')

    arg_list = region
    if email is not "":
        arg_list = region + " " + email

    child = Popen('/dragon_vpn/create.sh %s' % (arg_list), shell=True)
    child.communicate()[0]
    rc = child.returncode

    print('script resp code : ', rc)


def stop_vpn(region):
    print('Saying goodbye to the VPN')
    arg_list = region
    child = Popen('/dragon_vpn/destroy.sh' % (arg_list), shell=True)
    child.communicate()[0]
    rc = child.returncode

    print('script resp code : ', rc)


def parse_region(words_to_skip, message):

    words = []
    w_index = 0
    index = words_to_skip
    while index < len(message):
        words.append(message[index])
        index += 1
        w_index += 1

    if len(words) > 0:
        regions = aws_region_finder.aws_regions

        for word in words:
            for region in regions:
                if word == region:
                    return word

    return ''


def parse_email(words_to_skip, message):

    words = []
    w_index = 0
    index = words_to_skip
    while index < len(message):
        words.append(message[index])
        index += 1
        w_index += 1

    if len(words) > 0:

        for word in words:
            if '@' in word:
                if 'mailto' in word:
                    email_parts = str(word).split('|')
                    unparsed_email = email_parts[1]
                    l = len(unparsed_email)
                    email = unparsed_email[:l-1]
                    return str(email).strip()
                else:
                    return str(word).strip()

    return ''


def handle_command(command, channel, message):

    response = response_generator.get_action_unknown_response()
    print('Channel: ', channel)
    if command in COMMANDS:
        if command == "hi":
            response = "Hello. I am the mighty FoeHammer :crossed_swords:"
            slack_messenger.send_message(channel, response)
        else:
            slack_messenger.send_message(channel, response_generator.get_performing_action_response())

            print('command: ', command)
            if str(command).startswith("start vpn"):
                words_to_skip = 3
                region = parse_region(words_to_skip, message)
                email_address = parse_email(words_to_skip, message)
                if region is not '':
                    print('Email: ', email_address)
                    start_vpn(region, email_address)
                    response = command + " is done"
                else:
                    response = "Where am I meant to make this?"
                slack_messenger.send_message(channel, response)
            elif command == "stop vpn":
                words_to_skip = 3
                region = parse_region(words_to_skip, message)
                if region is not '':
                    stop_vpn(region)
                    response = "The vpn has been let go."
                else:
                    response = "As mighty as I may be, I'm not a mind reader. " \
                              "Best let me know where I'm bringing the pain."

                slack_messenger.send_message(channel, response)
            elif command == "whats going on?":
                response = "I'm not that clever yet."
                slack_messenger.send_message(channel, response)
    else:
        slack_messenger.send_message(channel, response)


if __name__ == "__main__":
    slack_token = os.environ.get('SLACK_TOKEN')
    if slack_token is not '' and slack_messenger.init_connection():
        print("dvpn bot is up and running ... feel the force of dragon wind")

        vpnbot_id = slack_messenger.get_bot_id()
        mention_regex = vpnbot_id

        while True:
            try:
                channel, command, message = parse_bot_message(slack_messenger.read_message(), vpnbot_id)
                if command:
                    handle_command(command, channel, message)
            except Exception, e:
                print ('Error executing command', str(e))
                slack_messenger.send_message(channel, response_generator.get_failed_action_response())
                slack_messenger.auth_client()

            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed :( Best check network and SLACK_TOKEN and that.")
