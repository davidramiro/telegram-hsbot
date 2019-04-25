# telegram-hsbot

A silly Telegram bot for groups written in Python. This is an early WIP with only the most basic functions published.

### Requirements
- Python 3.6

### Libraries used
- [python-telegram-bot](https://github.com/python-telegram-bot)
- [captionbot](https://github.com/krikunts/captionbot)
- [gTTS](https://github.com/pndurette/gTTS)

## Usage
 - `sudo pip3 install -r requirements.txt`
 - Add your bot token to `config.yml`
 - Adjust the config to your needs
 - Add content to the `/data/` folder
 - Start the bot: `python3 hsbot.py`

### Functions:
  - `describe`: Use Microsoft's CaptionBot AI to describe images
  - `dynamic_reply`: Reply to certain keywords with randomly picked audio, video and images
  - `rand_image`: Reply with random images, using different subdirectories corresponding to the context
  - `rate`: Get a random rating
  - `tts`: Use Google TTS to read out replies or context
  - `voice_reply`: Listen for certain keywords and reply with a voice message

### Todo:
- [ ] `scale` - Context aware scaling of images
- [ ] `glitch` - Glich jpg and png images
- [ ] `count` - Listen for & count specific keywords, print out messages on certain milestones
