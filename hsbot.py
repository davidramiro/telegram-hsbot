#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import time
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from telegram import ChatAction
import yaml
from modules import voice_reply, dynamic_reply, rate, describe, tts, rand_image

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

count_keywords = []
keyword_list = []


def start(update, context):
    """
    Respond to /start message
    """
    update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    update.message.reply_voice(voice=open(
        'data/audio/start.ogg', 'rb'), quote=True)


def help(update, context):
    """
    Respond to /help message
    """
    # Parse help text
    with open("data/help.txt", "r", encoding="UTF-8") as helpfile:
        help_text = helpfile.read()
        print("Help textfile imported")
    update.message.reply_text(help_text, parse_mode="Markdown")


def error(update, context):
    """
    Log errors caused by updates.
    """
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def message_parser(update, context):
    """
    Parse non-command message for certain contents
    """
    if dyn_reply_message is True:
        for dyn_keyword in config["features"]["dynamic_reply"]["commands"]:
            if dyn_keyword in update.message.text.lower():
                dynamic_reply.dyn_reply(update, context)

    if rand_image_message is True:
        for image_keyword in config["features"]["rand_image"]["commands"]:
            if image_keyword in update.message.text.lower():
                rand_image.reply_image(update, context, image_keyword)

    for voice_keyword in config["features"]["voice_reply"]["commands"]:
        if voice_keyword in update.message.text.lower():
            voice_reply.reply(update, context)

    for keyword in count_keywords:
        if keyword in update.message.text.lower():
            init_occurences = update.message.text.lower().count(keyword)
            for n in range(0, init_occurences):
                keyword_list.append(keyword)
                occurences = keyword_list.count(keyword)
                occur_str = str(occurences)
                if len(occur_str) > 1:
                    for j in range (0, 9):
                        number_times = int(occur_str.count(str(j)))
                        str_length = len(occur_str)
                        if number_times == str_length:
                            update.message.reply_text("*" + keyword + "*" + \
                            " count: " + str(occurences) + ".\n_Repdigit!_"\
                            , quote=True, parse_mode='Markdown')


def main():
    # Parse config
    global config
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    key = config["keys"]["telegram_token"]
    use_proxy = config["general"]["use_proxy"]["enabled"]
    for keyword in config["features"]["count"]["keywords"]:
        count_keywords.append(keyword)
    if use_proxy is True:
        proxy_url = config["general"]["use_proxy"]["proxy_url"]
    systemd_delay = config["general"]["use_systemd_delay"]
    global rand_image_message, dyn_reply_message
    dyn_reply_command = config["features"]["dynamic_reply"]["use_command_handler"]
    dyn_reply_message = config["features"]["dynamic_reply"]["use_message_handler"]
    rand_image_command = config["features"]["rand_image"]["use_command_handler"]
    rand_image_message = config["features"]["rand_image"]["use_message_handler"]

    # Small delay to make linux systemd work
    if systemd_delay is True:
        time.sleep(10)

    if use_proxy is True:
        updater = Updater(key, use_context=True, request_kwargs={'proxy_url': proxy_url})
    else:
        updater = Updater(key, use_context=True)
    dp = updater.dispatcher

    # Handle static commands commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # Add command parsers according to config
    if dyn_reply_command is True:
        for command in config["features"]["dynamic_reply"]["commands"]:
            dp.add_handler(CommandHandler(command, dynamic_reply.dyn_reply))

    if rand_image_command is True:
        for command in config["features"]["rand_image"]["commands"]:
            dp.add_handler(CommandHandler(command, dynamic_reply.dyn_reply))

    for command in config["features"]["rate"]["commands"]:
        dp.add_handler(CommandHandler(command, rate.get_rating))

    for command in config["features"]["describe"]["commands"]:
        dp.add_handler(CommandHandler(command, describe.reply_caption))

    for command in config["features"]["tts"]["commands"]:
        dp.add_handler(CommandHandler(command, tts.reply_tts))

    # Send text messages to the parser
    dp.add_handler(MessageHandler(Filters.text, message_parser))

    # Start the bot
    updater.start_polling()

    # Run until CTRL+C (or SIGTERM, etc.)
    updater.idle()


if __name__ == '__main__':
    main()
