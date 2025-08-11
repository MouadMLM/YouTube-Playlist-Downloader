#!/usr/bin/env python3
"""
YouTube Playlist Downloader with IDM Integration
Developed by: Mouadev (Updated by Grok for reliability)

Usage:
1. Install dependencies: pip install --upgrade yt-dlp pywin32
2. Ensure Internet Download Manager (IDM) is installed and running
3. Save this script as ytdown.py
4. Run: python ytdown.py
"""

import os
import re
import subprocess
import yt_dlp
import time
import sys
import win32gui
import win32con
from pathlib import Path

class IDMDownloader:
    """Class to handle IDM integration for downloads."""
    
    def __init__(self):
        self.idm_path = self.find_idm_path()
        if not self.idm_path:
            print("IDM not found! Please install Internet Download Manager.")
            sys.exit(1)
        print(f"Found IDM at: {self.idm_path}")
    
    def find_idm_path(self):
        """Find IDM installation path."""
        possible_paths = [
            r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe",
            r"C:\Program Files\Internet Download Manager\IDMan.exe",
            r"C:\IDM\IDMan.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        try:
            result = subprocess.run(['where', 'IDMan.exe'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        
        return None
    
    def minimize_idm_window(self):
        """Minimize the IDM window if it is open."""
        try:
            # Find the IDM window by partial title match
            def enum_windows_callback(hwnd, windows):
                title = win32gui.GetWindowText(hwnd).lower()
                if "internet download manager" in title:
                    windows.append(hwnd)
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd in windows:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                print("  Minimized IDM window")
        except Exception as e:
            print(f"  Could not minimize IDM window: {e}")
    
    def download_with_idm(self, url, output_path, filename):
        """Download file using IDM."""
        try:
            full_path = os.path.join(output_path, filename)
            cmd = [
                self.idm_path,
                '/d', url,
                '/p', output_path,
                '/f', filename,
                '/n',
                '/s',
            ]
            print(f"  Starting IDM download: {filename}")
            subprocess.run(cmd, capture_output=True, text=True)
            time.sleep(3)
            
            # Minimize IDM window after starting download
            self.minimize_idm_window()
            
            if os.path.exists(full_path) or self.is_idm_downloading(output_path, filename):
                print(f"  ✓ IDM download started: {filename}")
                return True
            else:
                print(f"  ⚠ IDM may have started (check IDM interface): {filename}")
                return True
        except Exception as e:
            print(f"  ✗ IDM error: {e}")
            return False
    
    def is_idm_downloading(self, output_path, filename):
        """Check if IDM is downloading the file."""
        try:
            temp_files = [f for f in os.listdir(output_path) if f.endswith('.idm') and filename in f]
            return len(temp_files) > 0
        except:
            return False
    
    def wait_for_downloads(self, save_path, timeout=300):
        """Wait for IDM downloads to complete."""
        print("\nWaiting for IDM downloads to complete...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq IDMan.exe'], 
                                      capture_output=True, text=True)
                temp_files = [f for f in os.listdir(save_path) if f.endswith('.idm')]
                if 'IDMan.exe' not in result.stdout or not temp_files:
                    print("No active IDM downloads found.")
                    break
                print(f"IDM still downloading... ({len(temp_files)} active)")
                time.sleep(10)
            except:
                break
        if time.time() - start_time >= timeout:
            print("Timeout waiting for downloads.")

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
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if match:
        playlist_id = match.group(1)
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    return url

def get_playlist_info(url):
    """Get playlist information and video URLs."""
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': '1-1000',
        'quiet': False,  # Enable verbose output for debugging
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' not in info:
                print("No playlist found or invalid URL.")
                print(f"Debug info: {info}")
                return None, []
            playlist_title = info.get('title', 'Unknown Playlist')
            entries = [entry for entry in info['entries'] if entry is not None]
            return playlist_title, entries
    except Exception as e:
        print(f"Error extracting playlist info: {str(e)}")
        return None, []

def get_video_download_url(video_id, quality_format):
    """Get direct download URL for video using yt-dlp."""
    try:
        ydl_opts = {
            'format': quality_format,
            'quiet': True,
            'no_warnings': True,
        }
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            if 'url' in info:
                return info['url'], info.get('ext', 'mp4')
            elif 'formats' in info and info['formats']:
                best_format = info['formats'][-1]
                return best_format['url'], best_format.get('ext', 'mp4')
        return None, None
    except Exception as e:
        print(f"  Error getting download URL: {e}")
        return None, None

def download_video_with_idm(video_info, save_path, quality_format, downloaded_files, idm_downloader):
    """Download a single video using IDM or fall back to yt-dlp."""
    try:
        video_id = video_info.get('id', 'unknown')
        video_title = sanitize_filename(video_info.get('title', f'video_{video_id}'))
        
        for ext in ['.mp4', '.webm', '.mkv', '.flv']:
            if f"{video_title}{ext}" in downloaded_files:
                print(f'Skipping "{video_title}" - already exists')
                return True
        
        print(f'Processing: {video_title}')
        download_url, file_ext = get_video_download_url(video_id, quality_format)
        
        if not download_url:
            print(f"  ✗ Could not get download URL, falling back to yt-dlp")
            ydl_opts = {
                'format': quality_format,
                'outtmpl': os.path.join(save_path, f"{video_title}.%(ext)s"),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            print(f"  ✓ Downloaded with yt-dlp: {video_title}")
            return True
        
        filename = f"{video_title}.{file_ext}"
        return idm_downloader.download_with_idm(download_url, save_path, filename)
    except Exception as e:
        print(f"  ✗ Error processing video: {e}")
        return False

def get_existing_files(directory):
    """Get list of existing video files in directory."""
    video_extensions = ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']
    return [f for f in os.listdir(directory) if any(f.lower().endswith(ext) for ext in video_extensions)]

def main():
    """Main function to run the playlist downloader."""
    print('YOUTUBE PLAYLIST DOWNLOADER WITH IDM')
    print('Developed by: Mouadev (Updated for reliability)')
    print('=' * 50)
    
    try:
        idm_downloader = IDMDownloader()
    except SystemExit:
        return
    
    url = input("Enter YouTube playlist URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return
    
    url = clean_playlist_url(url)
    print(f"Using playlist URL: {url}")
    
    print('\nQuality options:')
    print('1. Best quality available')
    print('2. 720p (if available)')
    print('3. 480p (if available)')
    print('4. 360p (if available)')
    
    choice = input("Choose quality (1-4, default: 2): ").strip()
    quality_formats = {
        '1': 'best',
        '2': 'best[height<=720]/best',
        '3': 'best[height<=480]/best',
        '4': 'best[height<=360]/best',
    }
    quality_names = {
        '1': 'Best quality',
        '2': '720p or best available',
        '3': '480p or best available',
        '4': '360p or best available',
    }
    quality_format = quality_formats.get(choice, 'best[height<=720]/best')
    print(f'Selected: {quality_names.get(choice, "720p or best available")}')
    
    print('\nExtracting playlist information...')
    playlist_title, entries = get_playlist_info(url)
    
    if not entries:
        print("No videos found or unable to access playlist.")
        return
    
    print(f'Playlist: {playlist_title}')
    print(f'Found {len(entries)} videos')
    
    # Use Downloads folder with a subfolder named after the playlist
    folder_name = sanitize_filename(playlist_title)[:50] or "youtube_playlist"
    save_path = os.path.join(os.path.expanduser("~"), "Downloads", folder_name)
    os.makedirs(save_path, exist_ok=True)
    print(f'Download directory: {save_path}')
    
    existing_files = get_existing_files(save_path)
    if existing_files:
        print(f'Found {len(existing_files)} existing files')
    
    print(f'\nStarting downloads...\n')
    successful_downloads = 0
    failed_downloads = 0
    skipped_downloads = 0
    
    for i, video_info in enumerate(entries, 1):
        print(f'[{i}/{len(entries)}]', end=' ')
        if video_info is None:
            print('Skipping unavailable video')
            skipped_downloads += 1
            continue
        result = download_video_with_idm(video_info, save_path, quality_format, existing_files, idm_downloader)
        if result:
            successful_downloads += 1
        else:
            failed_downloads += 1
        print()
        time.sleep(1)
    
    if successful_downloads > 0:
        print(f"\nStarted {successful_downloads} downloads.")
        wait_choice = input("Wait for downloads to complete? (y/n, default: y): ").strip().lower()
        if wait_choice != 'n':
            idm_downloader.wait_for_downloads(save_path)
    
    print('=' * 50)
    print('DOWNLOAD PROCESS COMPLETE!')
    print(f'Started: {successful_downloads}')
    print(f'Failed: {failed_downloads}')
    print(f'Skipped: {skipped_downloads}')
    print(f'Total videos processed: {len(entries)}')
    print(f'Files saved to: {save_path}')
    print('\nCheck IDM or Downloads folder for progress.')

if __name__ == "__main__":
    main()