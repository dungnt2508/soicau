from .. import socketio
from flask_socketio import emit, join_room, leave_room
from flask import current_app, session
from flask_login import current_user
from . import bp

# from ..db import add_sicbo, predict_sicbo

# potential negative responses
negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry", "không", "đéo", "méo", "cút")
# keywords for exiting the conversation
exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "thoát")
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


@socketio.on("join_room")
def handle_join_room(data):
    current_app.logger.info("{} has join room {}".format(data["username"], data["room"]))
    join_room(data["room"])
    socketio.emit("join_room_announcement", data, room=data["room"])


@socketio.on("send_message")
def handle_send_message(data):
    msg = ''
    try:

        current_app.logger.info("{} ở room {} đã gửi msg : {}".format(data["username"], data["room"], data["message"]))

        if data["message"].lower() in negative_responses:
            data["reply"] = "Ok, Snake chúc bạn một ngày tốt lành"
        else:
            reply_message(data)

        print(data)

        emit("receive_message", data)
    except Exception as e:
        str(e)


# Define .make_exit() here:
def make_exit(reply):
    for exit_command in exit_commands:
        if exit_command in reply:
            return True
    return False


# Define .chat() next:
def reply_message(data):
    reply = data["message"].lower()
    data["reply"] = "Ok, Snake chúc bạn một ngày tốt lành 2"
    if not make_exit(reply):
        data["reply"] = "Ok, tiếp tục"

    return data