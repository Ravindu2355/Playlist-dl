import os
from pyrogram import Client, filters
from pyrogram.types import Message
from downloader import download_video, get_playlist_videos, generate_thumbnail, compress_video

# Bot configuration
API_ID = int(os.getenv("apiid"))
API_HASH = os.getenv("apihash")
BOT_TOKEN = os.getenv("tk")

app = Client("youtube_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Welcome to the YouTube Downloader Bot! 🎥\n"
        "Send a YouTube video or playlist link to download as streamable Telegram videos."
    )

@app.on_message(filters.text)
async def download_handler(client, message: Message):
    url = message.text.strip()

    if "youtube.com/playlist" in url or "youtu.be/playlist" in url:
        st_msg = await message.reply_text("Processing playlist...")
        try:
            videos = get_playlist_videos(url)
            await st_msg.edit_text(f"Found {len(videos)} videos. Starting download...")

            for idx, video_url in enumerate(videos, start=1):
                prs_msg = await message.reply_text(f"Downloading video {idx}...")
                try:
                    file_path = download_video(video_url)
                    thumbnail_path = generate_thumbnail(file_path)
                    await prs_msg.edit_text("compressing video...")
                    compressed_video_path = compress_video(file_path)
                    
                    await prs_msg.edit_text(f"Uploading video {idx}...")
                    await client.send_video(
                        chat_id=message.chat.id,
                        video=compressed_video_path,
                        thumb=thumbnail_path,
                        caption=f"Video {idx} from playlist.",
                        supports_streaming=True,
                    )
                    os.remove(file_path)
                    os.remove(thumbnail_path)
                    await prs_msg.delete()
                except Exception as e:
                    await prs_msg.edit_text(f"Error with video {idx}: {str(e)}")
            await message.reply_text("Playlist processing completed!✅️")
        except Exception as e:
            await st_msg.edit_text(f"Error processing playlist: {str(e)}")
    elif "youtube.com" in url or "youtu.be" in url:
        st_msg = await message.reply_text("Downloading video...")
        try:
            file_path = download_video(url)
            thumbnail_path = generate_thumbnail(file_path)
            await st_msg.edit_text("compressing video...")
            compressed_video_path = compress_video(file_path)

            await st_msg.edit_text("Uploading video...")
            await client.send_video(
                chat_id=message.chat.id,
                video=compressed_video_path,
                thumb=thumbnail_path,
                caption="Here is your video.",
                supports_streaming=True,
            )
            os.remove(file_path)
            os.remove(thumbnail_path)
            await st_msg.delete()
        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
    else:
        await st_msg.edit_text("Invalid URL. Please send a valid YouTube link.")

app.run()
