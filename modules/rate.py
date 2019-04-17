#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import yaml
from datetime import datetime
from telegram.ext import CommandHandler
from telegram import ChatAction


ratings = []


def get_rating(update, context):
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    for config_rating in config["features"]["rate"]["ratings"]:
        ratings.append(config_rating)
    update.message.chat.send_action(ChatAction.TYPING)
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    rating = random.choice(ratings)
    update.message.reply_text("🤔 I rate this " + rating)
    print(current_time, ">", "/rate", ">", update.message.from_user.username)
