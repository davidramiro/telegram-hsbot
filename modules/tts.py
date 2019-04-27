#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import yaml
from telegram.ext.callbackcontext import CallbackContext
from telegram import ChatAction
from gtts import gTTS




def reply_tts(update, context: CallbackContext):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    update.message.chat.send_action(ChatAction.TYPING)
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    lang = config["features"]["tts"]["language"]
    path = config["features"]["tts"]["path"]
    reply = update.message.reply_to_message
    if reply is None:
        text = "".join(context.args)
    elif reply.text is not None:
        text = reply.text
    else:
        return
    if len(text) == 0:
        update.message.reply_text("Type in some text.")
        return
    tts = gTTS(text, lang)
    tts.save(path + filename + ".mp3")
    with open(path + filename + ".mp3", "rb") as speech:
        update.message.reply_voice(speech, quote=True)
    print(current_time, ">", "/say", ">", update.message.from_user.username)
    os.remove(path + filename + ".mp3")
