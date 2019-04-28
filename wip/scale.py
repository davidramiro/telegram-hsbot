#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import subprocess
import os
import requests
import yaml
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.dispatcher import run_async
from telegram import ChatAction



@run_async
def liquid(update, context: CallbackContext):
    """
    Rescale an image using liquid rescale (also known as content aware scale)
    """
    # get temp directory and size from config
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    path = config["features"]["scale"]["tmp_path"]
    scale_res = config["features"]["scale"]["size"]
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")

    # check for parameter in message
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

    # get the image
    if reply is None:
        extension = ".jpg"
        context.bot.getFile(update.message.photo[-1].file_id).download(path + filename + extension)
    # Entities; url, text_link
    if reply.entities is not None:
        urls = (extract_url(x, reply.text) for x in reply.entities)
        images = [x for x in urls if is_image(x)]
        if len(images) > 0:
            extension = is_image(images[0])
            r = requests.get(images[0])  # use only first image url
            with open(path + filename + extension, "wb") as f:
                f.write(r.content)
    # Document
    if reply.document is not None and is_image(reply.document.file_name):
        extension = is_image(reply.document.file_name)
        context.bot.getFile(reply.document.file_id).download(path + filename + extension)
    # Sticker
    if reply.sticker is not None:
        extension = ".webp"
        context.bot.getFile(reply.sticker.file_id).download(path + filename + extension)
    # Photo in reply
    if reply.photo is not None:
        extension = ".jpg"
        context.bot.getFile(reply.photo[-1].file_id).download(path + filename + extension)

    # liquid rescale via ImageMagick
    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    size = str(100 - (power / 1.3))
    absolute_path = os.path.abspath(path)
    x = "convert " + absolute_path + "/" + filename + extension + " -liquid-rescale " + \
         size + "%x" + size + "% -resize " + scale_res + "x" + scale_res + " " + \
         absolute_path + "/" + filename + "-liq.jpg"
    subprocess.run(x, shell=True)

    # TODO: handle mp4
    #if extension == ".mp4":
    #    mp4fix = "ffmpeg -loglevel panic -i " + path + name + extension + \
    #              " -an -vf scale=trunc(iw/2)*2:trunc(ih/2)*2 \
    #              -pix_fmt yuv420p -c:v libx264 -profile:v high -level:v 2.0 " \
    #              + path + name + "_mp4" + extension + " -y"
    #    subprocess.run(mp4fix, shell=True)
    #    os.remove(path+name+extension)
    #    name = name + "_mp4"

    # send scaled image and remove temporary files
    with open(path + filename + "-liq" + extension, "rb") as selected:
        update.message.reply_photo(selected, quote=True)
    os.remove(path + filename + extension)
    os.remove(path + filename + "-liq.jpg")
    print(current_time, ">", "/scale", ">", update.message.from_user.username)




def extract_url(entity, text):
    """
    Extract an URL from the message
    """
    if entity["type"] == "text_link":
        return entity["url"]
    elif entity["type"] == "url":
        offset = entity["offset"]
        length = entity["length"]
        return text[offset:offset+length]
    else:
        return None

def is_image(path):
    """
    Check if the file is an image
    """
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".tif", ".bmp", ".mp4")
    if path is None:
        return False
    for i in image_extensions:
        if path.casefold().endswith(i):
            ext = i
            return ext
    return False
