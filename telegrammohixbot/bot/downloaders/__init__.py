"""
Downloader implementations for each supported platform.

Each downloader module exposes a single async function that:
- Accepts a URL and target download directory
- Uses yt-dlp Python API to download the best-quality MP4
- Returns the path to the downloaded file
"""

