#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import yaml
from telegram import ChatAction


def reply(update, context):
    """
    Select a random file and set it properly according to the filetype
    """
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    file = config["features"]["voice_reply"]["file"]
    with open(file, "rb") as speech:
        update.message.reply_voice(speech, quote=True)
    print(current_time, ">", "voice_reply", ">",
          update.message.from_user.username)
