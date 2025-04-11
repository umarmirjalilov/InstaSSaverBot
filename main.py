import os
import requests
from telegram.ext import Updater, CommandHandler
from yt_dlp import YoutubeDL
from shazamio import Shazam
from pydub import AudioSegment

# Telegram bot token
TOKEN = os.getenv("BOT_TOKEN")

# Instagram video yuklash
def download_video(update, context):
    url = context.args[0]
    if not url:
        update.message.reply_text("Iltimos, Instagram video URL manzilini yuboring.")
        return
    video_info = get_video(url)
    if video_info:
        update.message.reply_video(video_info['video_url'])
        update.message.reply_text(f"Videodagi musiqa: {video_info['music']}")
    else:
        update.message.reply_text("Video topilmadi.")

def get_video(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get('url')
        music = get_music_from_video(video_url)
        return {'video_url': video_url, 'music': music}

# Musiqani aniqlash
def get_music_from_video(video_url):
    shazam = Shazam()
    audio = requests.get(video_url)
    audio_file = "temp.mp3"
    with open(audio_file, 'wb') as f:
        f.write(audio.content)
    
    audio_segment = AudioSegment.from_mp3(audio_file)
    music = shazam.recognize_song(audio_segment)
    return music.get('track', {}).get('title', 'Musiqa aniqlanmadi')

# Start komandasi
def start(update, context):
    update.message.reply_text('Assalomu alaykum! Instagram video linkini yuboring.')

# Botni ishga tushurish
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
