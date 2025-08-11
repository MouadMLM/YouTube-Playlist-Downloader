#!/usr/bin/env python3
"""
YouTube Playlist Downloader using yt-dlp only (no IDM)
Developed by: Mouadev (ffmpeg)

Usage:
1. Install dependencies: pip install --upgrade yt-dlp
2. Save this script as ytdown_no_idm.py
3. Run: python ytdown_no_idm.py
"""

import os
import re
import time
import yt_dlp

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    filename = re.sub(r'\s+', ' ', filename).strip()
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def clean_playlist_url(url):
    """Extract playlist ID and return a clean playlist URL."""
    import re
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if match:
        playlist_id = match.group(1)
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    return url

def get_playlist_info(url):
    """Get playlist info and videos."""
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': '1-1000',
        'quiet': False,
        'no_warnings': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' not in info:
                print("No playlist found or invalid URL.")
                return None, []
            playlist_title = info.get('title', 'Unknown Playlist')
            entries = [entry for entry in info['entries'] if entry is not None]
            return playlist_title, entries
    except Exception as e:
        print(f"Error extracting playlist info: {e}")
        return None, []

def get_existing_files(directory):
    """Get list of existing video files in directory."""
    video_extensions = ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']
    return [f for f in os.listdir(directory) if any(f.lower().endswith(ext) for ext in video_extensions)]

def download_video(video_info, save_path, quality_format, existing_files):
    """Download video with yt-dlp, skip if exists."""
    try:
        video_id = video_info.get('id', 'unknown')
        video_title = sanitize_filename(video_info.get('title', f'video_{video_id}'))

        # Skip if file exists
        for ext in ['.mp4', '.webm', '.mkv', '.flv']:
            if f"{video_title}{ext}" in existing_files:
                print(f'Skipping "{video_title}" - already exists')
                return True

        print(f'Downloading: {video_title}')
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            'format': quality_format,
            'outtmpl': os.path.join(save_path, f"{video_title}.%(ext)s"),
            'merge_output_format': 'mp4',  # Merge into mp4 container
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✓ Downloaded: {video_title}")
        return True
    except Exception as e:
        print(f"✗ Error downloading {video_info.get('title', 'unknown')}: {e}")
        return False

def main():
    print('YOUTUBE PLAYLIST DOWNLOADER (yt-dlp only)')
    print('Developed by: Mouadev')
    print('=' * 50)

    url = input("Enter YouTube playlist URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return

    url = clean_playlist_url(url)
    print(f"Using playlist URL: {url}")

    quality_format = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'
    print('Selected quality: 1080p max (merged if needed)')

    print('\nExtracting playlist information...')
    playlist_title, entries = get_playlist_info(url)
    if not entries:
        print("No videos found or unable to access playlist.")
        return

    print(f'Playlist: {playlist_title}')
    print(f'Found {len(entries)} videos')

    folder_name = sanitize_filename(playlist_title)[:50] or "youtube_playlist"
    save_path = os.path.join(os.path.expanduser("~"), "Downloads", folder_name)
    os.makedirs(save_path, exist_ok=True)
    print(f'Download directory: {save_path}')

    existing_files = get_existing_files(save_path)
    if existing_files:
        print(f'Found {len(existing_files)} existing files')

    print('\nStarting downloads...\n')

    success_count = 0
    fail_count = 0
    skipped_count = 0

    for i, video_info in enumerate(entries, 1):
        print(f'[{i}/{len(entries)}]', end=' ')
        if video_info is None:
            print('Skipping unavailable video')
            skipped_count += 1
            continue
        if download_video(video_info, save_path, quality_format, existing_files):
            success_count += 1
        else:
            fail_count += 1
        print()
        time.sleep(1)

    print('=' * 50)
    print('DOWNLOAD PROCESS COMPLETE!')
    print(f'Successful: {success_count}')
    print(f'Failed: {fail_count}')
    print(f'Skipped: {skipped_count}')
    print(f'Total videos processed: {len(entries)}')
    print(f'Files saved to: {save_path}')
    print('\nCheck your Downloads folder for videos.')

if __name__ == "__main__":
    main()
