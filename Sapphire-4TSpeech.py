__author__ = "Created By:\nChristian Skye aka Dracomenda"
__copyright__ = "Copyright Christian Skye, \nSapphire Imagination Society 2024"
__license__ = "Distributed under: \nMIT License"
__title__ = "Sapphire 4TSpeech Tool"

__LOGO__ = "      ^\n     # #\n    ## ##\n  ####0####\n#####0O0#####\n  ####0####\n    ## ##\n     # #\n      v"

from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from TikTokLive.events import ConnectEvent, GiftEvent, CommentEvent
from gtts import gTTS
import os
import subprocess
import tempfile
import asyncio
import re
import websockets

# ANSI escape codes for coloring console output
CYAN = '\033[96m'
RESET = '\033[0m'
SUBB = '\033[91m'

# Sanitize input by allowing only safe characters
def sanitize_username(username):
    return re.sub(r'[^a-zA-Z0-9_.]', '', username)

# Change this to your @Username
tiktok_id = input("input the user ID of the livestream you wish to connect to\n : | ")
sub_only = input("Do you only want to see subscriber chat?\nTrue or False | : ")
sanitized_tiktok_id = sanitize_username(tiktok_id)
client = TikTokLiveClient(unique_id="@" + sanitized_tiktok_id)

def display_user_badges(user):
    if hasattr(user, 'badge_list'):
        for badge in user.badge_list:
            badge_icon = badge.combine.icon.url_list[0] if badge.combine.icon.url_list else "No icon"
            if "fan_badge" in badge_icon:
                print(f"{event.user.unique_id} is a Channel Member")

def play_audio(file_path):
    try:
        subprocess.run(["paplay", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    client.logger.info(f"Connected to @{event.unique_id}!")

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    client.logger.info("Received a gift!")
    if event.gift.streakable and not event.streaking:
        print(f"{event.user.unique_id} sent {event.repeat_count}x \"{event.gift.name}\"")
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.name}\"")

@client.on(CommentEvent)
async def on_chat(event: CommentEvent):
    user = event.user
    if hasattr(user, 'is_subscriber') and user.is_subscriber and "." in event.comment[0]:
        highlighted_comment = CYAN + f"{user.unique_id}: \"{event.comment}\"" + RESET
        print(highlighted_comment)
        tts = gTTS(text=event.comment[1:], lang='en')
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            tts.save(temp_file.name)
            play_audio(temp_file.name)
            os.unlink(temp_file.name)
    # Checks if the message is from a subscriber and adds a chat color to console
    elif hasattr(user, 'is_subscriber') and user.is_subscriber:
        sub_message = SUBB + f"{user.unique_id}: \"{event.comment}\"" + RESET
        print(sub_message)
    #Non-Subscriber messages
    else:
        if sub_only == "False":
            n=0
            if n/=4
            print(f"{user.unique_id} is not a subscriber")
            print(f"{user.unique_id}: \"{event.comment}\"")
            display_user_badges(user)
        else:
            pass

async def run_client():
    try:
        await client.connect()
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed unexpectedly. Reconnecting...")
        await asyncio.sleep(5)
        await run_client()
    except TypeError as e:
        print(f"An error occurred: {e}. Please check the username or try again later.")

if __name__ == '__main__':
    client.logger.setLevel(LogLevel.INFO.value)
    print("\n\nThe Sapphire Imagination Society Presents:\n\n__________________________________\n" + __title__ + "\n\n" + __author__ + "\n" + __copyright__ + "\n" + __license__ + "\n\n" + __LOGO__ + "\n\n")
    asyncio.get_event_loop().run_until_complete(run_client())
