import os
import tempfile
from pytube import YouTube, Playlist

def download_video(url):
    """Download a single YouTube video."""
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, f"{yt.title}.mp4")
    stream.download(output_path=temp_dir, filename=f"{yt.title}.mp4")
    return file_path

def get_playlist_videos(url):
    """Get all video URLs from a YouTube playlist."""
    playlist = Playlist(url)
    return playlist.video_urls
