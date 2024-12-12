import os
from pyrogram import Client, filters
from pyrogram.types import Message
from downloader import download_video, get_playlist_videos

# Bot configuration
API_ID = int(os.getenv("apiid"))
API_HASH = os.getenv("apihash")
BOT_TOKEN = os.getenv("tk")

app = Client("youtube_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Welcome to the YouTube Downloader Bot! 🎥\n"
        "Send a YouTube video or playlist link to download."
    )

@app.on_message(filters.text & ~filters.command)
async def download_handler(client, message: Message):
    url = message.text.strip()

    if "youtube.com/playlist" in url or "youtu.be/playlist" in url:
        await message.reply_text("Processing playlist...")
        try:
            videos = get_playlist_videos(url)
            await message.reply_text(f"Found {len(videos)} videos. Starting download...")

            for idx, video_url in enumerate(videos, start=1):
                await message.reply_text(f"Downloading video {idx}...")
                try:
                    file_path = download_video(video_url)
                    await message.reply_text(f"Uploading video {idx}...")
                    await client.send_document(chat_id=message.chat.id, document=file_path)
                    os.remove(file_path)
                except Exception as e:
                    await message.reply_text(f"Error with video {idx}: {str(e)}")
            await message.reply_text("Playlist processing completed!")
        except Exception as e:
            await message.reply_text(f"Error processing playlist: {str(e)}")
    elif "youtube.com" in url or "youtu.be" in url:
        await message.reply_text("Downloading video...")
        try:
            file_path = download_video(url)
            await message.reply_text("Uploading video...")
            await client.send_document(chat_id=message.chat.id, document=file_path)
            os.remove(file_path)
        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
    else:
        await message.reply_text("Invalid URL. Please send a valid YouTube link.")

app.run()
