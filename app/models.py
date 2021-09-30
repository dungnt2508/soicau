import re
import random
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, fullname, password):
        self.email = email
        self.fullname = fullname
        self.password = password

    def get_id(self):
        return self.email


class LasvegasBot:
    # potential negative responses
    negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
    # keywords for exiting the conversation
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    # random starter questions
    random_questions = (
        "Why are you here? ",
        "Are there many humans like you? ",
        "What do you consume for sustenance? ",
        "Is there intelligent life on this planet? ",
        "Does Earth have a leader? ",
        "What planets have you visited? ",
        "What technology do you have on this planet? "
    )

    def __init__(self):
        self.alienbabble = {'describe_planet_intent': [r'.*\s*your planet.*'],
                            'answer_why_intent': [r'why\sare.*'],
                            'cubed_intent': [r'.*cube.*(\d+)']
                            }

    # Define .greet() below:
    def greet(self, name):
        self.name = name

        will_help = 'Xin chào {}, tôi là SnakeBot v1 . Tôi có thể giúp gì cho bạn ? <br> <li class="breadcrumb-item"><a href="#">Home</a></li>'.format(self.name)

        return will_help

        # if will_help in self.negative_responses:
        #     print("Ok, have a nice Earth day!")
        #     return
        # self.chat()

    # Define .make_exit() here:
    def make_exit(self, reply):
        for exit_command in self.exit_commands:
            if exit_command in reply:
                print("Ok, have a nice Earth day! make_exit")
                return True
        return False

    # Define .chat() next:
    def chat(self):
        reply = input(random.choice(self.random_questions)).lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply))

    # Define .match_reply() below:
    def match_reply(self, reply):
        intent = ''

        for key, values in self.alienbabble.items():

            for regex_pattern in values:
                found_match = re.match(regex_pattern, reply)

                if found_match and key == "describe_planet_intent":

                    return self.describe_planet_intent()

                elif found_match and key == "answer_why_intent":

                    return self.answer_why_intent()

                elif found_match and key == "cubed_intent":

                    return self.cubed_intent(found_match.groups()[0])

        return self.no_match_intent()


    # Define .describe_planet_intent():
    def describe_planet_intent(self):
        responses = ("My planet is a utopia of diverse organisms and species. ", "I am from Opidipus, the capital of the Wayward Galaxies. ")
        return random.choice(responses)

    # Define .answer_why_intent():
    def answer_why_intent(self):
        responses = ("I come in peace.  ",
                     "I am here to collect data on your planet and its inhabitants. ",
                     "I heard the coffee is good.")
        return random.choice(responses)

    # Define .cubed_intent():
    def cubed_intent(self, number):
        number = int(number)
        cubed_number = number * number * number
        return f"The cube of {number} is {cubed_number}. Isn't that cool? "

    # Define .no_match_intent():
    def no_match_intent(self):
        responses = ("Please tell me more.",
                     "Tell me more! ",
                     "Why do you say that? ",
                     "I see. Can you elaborate?",
                     "Interesting. Can you tell me more? ",
                     "I see. How do you think? ",
                     "Why?",
                     "How do you think I feel when you say that?")
        return random.choice(responses)

# # Create an instance of AlienBot below:
# alient_bot = AlienBot()
# alient_bot.greet()

