#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint
from datetime import datetime
import os
import yaml
from telegram import ChatAction


def reply_image(update, context, image_keyword):
    """
    Post a random image from the path folder
    """
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)

    # set path according to config settings
    if config["features"]["rand_image"]["command_subfolder"] is True:
        path = config["features"]["rand_image"]["path"] + image_keyword + "/"
    else:
        path = config["features"]["rand_image"]["path"]

    files = os.listdir(path)
    filecount = len(files)

    # pick random image and send
    rand = randint(0, filecount - 1)
    result = files[rand]
    with open(path + str(result), "rb") as selected:
        update.message.reply_photo(selected, quote=True)
    print(current_time, ">", "rand_image: ", image_keyword, ">", selected,
          ">", update.message.from_user.username)
