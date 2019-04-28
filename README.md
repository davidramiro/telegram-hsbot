# telegram-hsbot

A silly Telegram bot for groups written in Python. This is an early WIP with only the most basic functions published.

### Requirements
- Python 3.6

### Dependencies
- [python-telegram-bot](https://github.com/python-telegram-bot)
- [captionbot](https://github.com/krikunts/captionbot)
- [gTTS](https://github.com/pndurette/gTTS)
- [ImageMagick](https://imagemagick.org/)

## Usage
 - Install required modules: `sudo pip3 install -r requirements.txt`
 - Install ImageMagick: `sudo apt install imagemagick`
 - Add your bot token to `config.yml`
 - Adjust the config to your needs
 - Add content to the `/data/` folder
 - Start the bot: `python3 hsbot.py`

### Features:
  - `count`: parse all messages and listen for certain keywords, message on "milestones"
  - `/describe`: Use Microsoft's CaptionBot AI to describe images
  - `dynamic_reply`: Reply to certain keywords with randomly picked audio, video and images
  - `rand_image`: Reply with random images, using different subdirectories corresponding to the context
  - `/rate`: Get a random rating
  - `/scale`: Liquid-rescale image, optional strength parameter of 0 to 100
  - `/say`: Use Google TTS to read out replies or context
  - `voice_reply`: Listen for certain keywords and reply with a voice message

### Todo:
- [x] `scale` - Context aware scaling of images - currently WIP, expect some bugs
- [ ] `glitch` - Glich jpg and png images
- [x] `count` - Listen for & count specific keywords, print out messages on certain milestones (currently using repdigits as milestones)
