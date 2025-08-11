# YouTube Playlist Downloader with IDM Integration by Mouadev

## Overview
This Python script downloads YouTube playlists using `yt-dlp` and integrates with Internet Download Manager (IDM) for faster downloads. It supports selecting video quality, skipping existing files, and automatically minimizing the IDM window. Downloads are saved to a subfolder in the user's Downloads directory, named after the playlist (sanitized for filesystem compatibility).

Developed by: Mouadev - 2025.

## Features
- Extracts playlist information and video URLs using `yt-dlp`.
- Downloads videos via IDM or falls back to `yt-dlp` if IDM fails.
- Supports quality options: Best, 720p, 480p, 360p.
- Skips already downloaded videos.
- Creates a subfolder in Downloads (e.g., `C:\Users\<YourUsername>\Downloads\<playlist_name>`).
- Minimizes the IDM window automatically after starting downloads using `pywin32`.
- Handles non-ASCII playlist titles (e.g., Arabic characters).
- Debug output for errors like "No playlist found or invalid URL".

## Requirements
- **Python 3.6+**: Includes standard library modules:
- **Internet Download Manager (IDM)**: Installed and running (path: `C:\Program Files (x86)\Internet Download Manager\IDMan.exe` or similar), you will find it in this repo . 
- **Python Dependencies** (in `requirements.txt`):
  - `yt-dlp`: For extracting and downloading YouTube videos.
  - `pywin32`: For minimizing the IDM window (provides `win32gui` and `win32con`).

## Installation
1. **Install IDM correctly**:
   </br>-Download & unzip the folder of idm app and follow instructions.
3. **Install Python**:
   - Download and install Python 3.6+ from [python.org](https://www.python.org/).
   - Ensure Python is added to your system PATH.
 
4. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt

## Contacts
-Telegram : https://t.me/Pilot2201
</br> -instagram
</br> -Email
