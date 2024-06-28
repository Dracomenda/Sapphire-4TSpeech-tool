__author__ = "Created By:\nChristian Skye aka Dracomenda"
__copyright__ = "Copyright Christian Skye, \nSapphire Imagination Society 2024"
__license__ = "Distributed under: \nMIT License"
__title__ = "Sapphire 4TSpeech Tool"

from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from TikTokLive.events import ConnectEvent, GiftEvent, CommentEvent
from gtts import gTTS
import os
import sys
import subprocess
import tempfile

# ANSI escape codes for coloring console output
CYAN = '\033[96m'
RESET = '\033[0m'

# Change this to your @Username
tiktok_id = input("input the user ID of the livestream you wish to connect to\n : | ")
client = TikTokLiveClient(unique_id="@" + tiktok_id)

def display_user_badges(user):
    if hasattr(user, 'badge_list'):
        #print(f"User {user.nickname} has the following badges:")
        for badge in user.badge_list:
            # Displaying badge details
            badge_icon = badge.combine.icon.url_list[0] if badge.combine.icon.url_list else "No icon"
            #print(f"- Type: {badge.display_type}, Icon URL: {badge_icon}, Additional Info: {badge.str}")
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
    user = event.user  # Define user here correctly
    #print(f"{user.unique_id}: \"{event.comment}\"")

    # Check if user is a subscriber and comment contains a "."
    if hasattr(user, 'is_subscriber') and user.is_subscriber and "*" in event.comment:
        # Highlight subscriber comments in cyan and adjust the comment to play
        highlighted_comment = CYAN + f"{user.unique_id}: \"{event.comment}\"" + RESET
        print(highlighted_comment)
        tts = gTTS(text=event.comment[1:], lang='en')  # Skip first char for TTS
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            tts.save(temp_file.name)
            play_audio(temp_file.name)
            os.unlink(temp_file.name)  # Clean up the temporary file
    else:
        print(f"{user.unique_id} is not a subscriber")
        # Print non-subscriber comments normally
        print(f"{user.unique_id}: \"{event.comment}\"")
        display_user_badges(user)

if __name__ == '__main__':
    client.logger.setLevel(LogLevel.INFO.value)  # Set log level to INFO
    print("\n\nThe Sapphire Imagination Society Presents:\n\n__________________________________\n" + __title__ + "\n\n" + __author__ + "\n" + __copyright__ + "\n" + __license__ + "\n\n")
    client.run()  # Connect to the TikTok live stream
