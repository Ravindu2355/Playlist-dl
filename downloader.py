import os
import tempfile
from moviepy.editor import VideoFileClip
import yt_dlp

def download_video(url):
    """Download a single YouTube video using yt-dlp."""
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

def get_playlist_videos(url):
    """Get all video URLs from a YouTube playlist using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(url, download=False)
        return [entry['url'] for entry in playlist_dict['entries']]


def generate_thumbnail(video_path):
    """Generate a thumbnail for the video using MoviePy."""
    clip = VideoFileClip(video_path)
    thumbnail_path = os.path.splitext(video_path)[0] + "_thumb.jpg"
    frame = clip.get_frame(clip.duration / 2)  # Get a frame from the middle of the video
    clip.close()

    from PIL import Image
    image = Image.fromarray(frame)
    image.save(thumbnail_path, "JPEG")
    return thumbnail_path
