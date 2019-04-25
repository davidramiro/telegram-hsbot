#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import mimetypes
from datetime import datetime
import logging
import requests
import yaml
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.dispatcher import run_async
from telegram import ChatAction
from modules.utils import extract_url, is_image
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

logger = logging.getLogger("captionbot")


@run_async
def reply_caption(update, context: CallbackContext):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    update.message.chat.send_action(ChatAction.TYPING)
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    path = config["features"]["describe"]["tmp_path"]
    output = os.path.join(path, filename)
    reply = update.message.reply_to_message
    if reply is None:
        extension = ".jpg"
        context.bot.getFile(
            update.message.photo[-1].file_id).download(output + extension)
        # return extension
    # Entities; url, text_link
    if reply.entities is not None:
        urls = (extract_url(x, reply.text) for x in reply.entities)
        images = [x for x in urls if is_image(x)]
        if len(images) > 0:
            extension = is_image(images[0])
            r = requests.get(images[0])  # use only first image url
            with open(output + extension, "wb") as f:
                f.write(r.content)
            # return extension
    # Document
    if reply.document is not None and is_image(reply.document.file_name):
        extension = is_image(reply.document.file_name)
        context.bot.getFile(reply.document.file_id).download(
            output + extension)
        # return extension
    # Sticker
    if reply.sticker is not None:
        extension = ".webp"
        context.bot.getFile(reply.sticker.file_id).download(output + extension)
        # return extension
    # Photo in reply
    if reply.photo is not None:
        extension = ".jpg"
        context.bot.getFile(
            reply.photo[-1].file_id).download(output + extension)
        # return extension
    c = CaptionBot()
    update.message.reply_text(c.file_caption(path + filename + extension))
    os.remove(path + filename + extension)
    print(current_time, ">", "/scale", ">", update.message.from_user.username)


class CaptionBotException(Exception):
    pass


class CaptionBot:
    UPLOAD_URL = "https://www.captionbot.ai/api/upload"
    MESSAGES_URL = "https://captionbot.azurewebsites.net/api/messages"

    @staticmethod
    def _resp_error(resp):
        if not resp.ok:
            data = resp.json()
            msg = "HTTP error: {}".format(resp.status_code)
            if type(data) == dict and "Message" in data:
                msg += ", " + data.get("Message")
            raise CaptionBotException(msg)

    def __init__(self):
        self.session = requests.Session()

    def _upload(self, filename):
        url = self.UPLOAD_URL
        mime = mimetypes.guess_type(filename)[0]
        name = os.path.basename(filename)
        files = {'file': (name, open(filename, 'rb'), mime)}
        resp = self.session.post(url, files=files)
        logger.debug("upload: {}".format(resp))
        self._resp_error(resp)
        res = resp.text
        if res:
            return res[1:-1]

    def url_caption(self, image_url):
        data = {
            "Content": image_url,
            "Type": "CaptionRequest",
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        url = self.MESSAGES_URL
        resp = self.session.post(url, data=json.dumps(data), headers=headers)
        logger.info("get_caption: {}".format(resp))
        if not resp.ok:
            return None
        res = resp.text[1:-1].replace('\\"', '"').replace('\\n', '\n')
        logger.info(res)
        return res

    def file_caption(self, filename):
        upload_filename = self._upload(filename)
        return self.url_caption(upload_filename)
