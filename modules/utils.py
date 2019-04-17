#!/usr/bin/python
# -*- coding: utf-8 -*-
# Credits to MadiNyan & Slko
import requests
import os.path
from telegram.ext.callbackcontext import CallbackContext


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


def get_image(update, context: CallbackContext, dl_path, filename):
    output = os.path.join(dl_path, filename)
    reply = update.message.reply_to_message
    if reply is None:
        extension = ".jpg"
        context.bot.getFile(update.message.photo[-1].file_id).download(output + extension)
        return extension
    # Entities; url, text_link
    if reply.entities is not None:
        urls = (extract_url(x, reply.text) for x in reply.entities)
        images = [x for x in urls if is_image(x)]
        if len(images) > 0:
            extension = is_image(images[0])
            r = requests.get(images[0])  # use only first image url
            with open(output+extension, "wb") as f:
                f.write(r.content)
            return extension
    # Document
    if reply.document is not None and is_image(reply.document.file_name):
        extension = is_image(reply.document.file_name)
        context.bot.getFile(reply.document.file_id).download(output + extension)
        return extension
    # Sticker
    if reply.sticker is not None:
        extension = ".webp"
        context.bot.getFile(reply.sticker.file_id).download(output+extension)
        return extension
    # Photo in reply
    if reply.photo is not None:
        extension = ".jpg"
        context.bot.getFile(reply.photo[-1].file_id).download(output + extension)
        return extension
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


def get_param(update, defaultvalue, min_value, max_value):
    if update.message.reply_to_message is not None:
        parts = update.message.text.split(" ", 1)
    elif update.message.caption is not None:
        parts = update.message.caption.split(" ", 1)
    else:
        return defaultvalue
    if len(parts) == 1:
        parameter = defaultvalue
    else:
        try:
            parameter = int(parts[1])
        except:
            update.message.reply_text("Paremeter needs to be a number!")
            return None
        if  parameter < min_value or parameter > max_value:
            errtext = "Baka, make it from " + str(min_value) + " to " + str(max_value) + "!"
            update.message.reply_text(errtext)
            return None
    return parameter


# custom filters for message handler
# photo with caption
def caption_filter(text):
    return lambda msg: bool(msg.photo) and bool(msg.caption) and msg.caption.startswith(text)


# text of choice
def text_filter(text):
    return lambda msg: bool(text in msg.text)
