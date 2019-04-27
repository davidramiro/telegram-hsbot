#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import subprocess
import os
import requests
#from utils import caption_filter, get_image, send_image, get_param, extract_url, is_image
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.dispatcher import run_async
from telegram import ChatAction

# TODO: parse path from config
# TODO: implement handle os.path.abspath() for subprocess
path = "./data/tmp/liq/"


@run_async
def liquid(update, context: CallbackContext):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    if update.message.reply_to_message is not None:
        parts = update.message.text.split(" ", 1)
    elif update.message.caption is not None:
        parts = update.message.caption.split(" ", 1)
    else:
        power = 60
    if len(parts) == 1:
        power = 60
    else:
        try:
            power = int(parts[1])
        except:
            update.message.reply_text("Paremeter has to be a number!")
            return
        if  power < 0 or power > 100:
            update.message.reply_text("Parameter has to be 0 to 100!")
            return
    reply = update.message.reply_to_message
    if reply is None:
        extension = ".jpg"
        context.bot.getFile(update.message.photo[-1].file_id).download(path + "tmp" + extension)
    # Entities; url, text_link
    if reply.entities is not None:
        urls = (extract_url(x, reply.text) for x in reply.entities)
        images = [x for x in urls if is_image(x)]
        if len(images) > 0:
            extension = is_image(images[0])
            r = requests.get(images[0])  # use only first image url
            with open(path + "tmp" + extension, "wb") as f:
                f.write(r.content)
    # Document
    if reply.document is not None and is_image(reply.document.file_name):
        extension = is_image(reply.document.file_name)
        context.bot.getFile(reply.document.file_id).download(path + "tmp" + extension)
    # Sticker
    if reply.sticker is not None:
        extension = ".webp"
        context.bot.getFile(reply.sticker.file_id).download(path + "tmp" + extension)
    # Photo in reply
    if reply.photo is not None:
        extension = ".jpg"
        context.bot.getFile(reply.photo[-1].file_id).download(path + "tmp" + extension)

    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    size = str(100 - (power / 1.3))
    x = "convert " + path + "tmp" + extension + " -liquid-rescale " + \
         size + "%x" + size + "% -resize 1000x1000 " + path + "tmp-liq" + extension
    subprocess.run(x, shell=True)
    if extension == ".mp4":
        mp4fix = "ffmpeg -loglevel panic -i " + path + name + extension + \
                  " -an -vf scale=trunc(iw/2)*2:trunc(ih/2)*2 \
                  -pix_fmt yuv420p -c:v libx264 -profile:v high -level:v 2.0 " \
                  + path + name + "_mp4" + extension + " -y"
        subprocess.run(mp4fix, shell=True)
        os.remove(path+name+extension)
        name = name + "_mp4"
    with open(path + "tmp-liq" + extension, "rb") as selected:
        update.message.reply_photo(selected, quote=True)
    os.remove(path + "tmp" + extension)
    os.remove(path + "tmp-liq" + extension)
    print(current_time, ">", "/scale", ">", update.message.from_user.username)




def extract_url(entity, text):
    if entity["type"] == "text_link":
        return entity["url"]
    elif entity["type"] == "url":
        offset = entity["offset"]
        length = entity["length"]
        return text[offset:offset+length]
    else:
        return None

def is_image(path):
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".tif", ".bmp", ".mp4")
    if path is None:
        return False
    for i in image_extensions:
        if path.casefold().endswith(i):
            ext = i
            return ext
    return False

def send_image(update, filepath, name, extension):
    photo_extensions = (".jpg", ".jpeg")
    doc_extensions = (".png", ".svg", ".tif", ".bmp", ".gif", ".mp4")
    sticker_extension = ".webp"
    for i in photo_extensions:
        if extension.endswith(i):
            with open(filepath + name + extension, "rb") as f:
                update.message.reply_photo(f)
            return True
    for i in doc_extensions:
        if extension.endswith(i):
            with open(filepath + name + extension, "rb") as f:
                update.message.reply_document(f)
            return True
    if extension.endswith(sticker_extension):
        with open(filepath + name + extension, "rb") as f:
            update.message.reply_sticker(f)
        return True
