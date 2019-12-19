import random

busy_responses = ["I'm busy", "Sorry. No can do busy at the moment",
                  "Gimme a couple more mins", "I'm doing something else right now",
                  "Busy", "gimme a break yo", "quite the task master anrn't we?",
                  "I'm working here. Why don't you do it yourself?", "Sorry, busy atm"
                  ]

performing_command_responses = ["As you command",
                                "As you wish", "ok", "Lets see...",
                                "On it!", "ok, doing this now", "I'll try",
                                "ok. I be doing this now."]


action_unknown = ["I'm not sure what you mean.",
                  "I'm confused",
                  "No",
                  "Why should I?",
                  "Whats in it for me?",
                  "What would you give for it?",
                  "You didn't say please.",
                  "... erm no"]

failed_action = ["I've failed. :disappointed:",
                 "I'm sorry but something went wrong",
                 "Why you get me to do stuff I can't do?",
                 "I totally tried but failed :disappointed:"]


def get_busy_response():
    return random.choice(busy_responses)


def get_performing_action_response():
    return random.choice(performing_command_responses)


def get_action_unknown_response():
    return random.choice(action_unknown)


def get_failed_action_response():
    return random.choice(failed_action)