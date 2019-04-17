#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from random import randint
import yaml
from telegram import ChatAction



def dyn_reply(update, context):
    """
    Select a random file and send it properly according to the filetype
    """
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    # Set path and select file
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    path = config["features"]["dynamic_reply"]["path"]
    files = os.listdir(path)
    filecount = len(files)
    rand = randint(0, filecount-1)
    result = files[rand]

    # Video
    if result.endswith(".mp4"):
        update.message.chat.send_action(ChatAction.UPLOAD_VIDEO)
        with open(path + result, "rb") as video:
            update.message.reply_video(video, quote=True)
        print(current_time, ">", "dynamic_reply", ">", update.message.from_user.username)

    # Audio
    if result.endswith("mp3") or result.endswith("ogg"):
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        with open(path + result, "rb") as speech:
            update.message.reply_voice(speech, quote=True)
        print(current_time, ">", "dynamic_reply", ">", update.message.from_user.username)

    # Photo
    if result.endswith("jpg") or result.endswith("png"):
        update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
        with open(path + result, "rb") as photo:
            update.message.reply_photo(photo, quote=True)
        print(current_time, ">", "dynamic_reply", ">", update.message.from_user.username)
