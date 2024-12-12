import os
import tempfile
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip

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
