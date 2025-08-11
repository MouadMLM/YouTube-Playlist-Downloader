# YouTube Playlist Downloader by Mouadev

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

<h2>Requirements</h2>
<ul>
  <li><strong>Python 3.6+</strong></li>
  <li><strong>Internet Download Manager (IDM)</strong> installed and running<br>
    Typical installation paths:<br>
    <code>C:\Program Files (x86)\Internet Download Manager\IDMan.exe</code> or<br>
    <code>C:\Program Files\Internet Download Manager\IDMan.exe</code><br>
    <em>(IDM installer is included in this repository)</em>
  </li>
  <li><strong>Python dependencies</strong> (see <code>requirements.txt</code>):<br>
    <ul>
      <li><code>yt-dlp</code> — for downloading YouTube videos</li>
      <li><code>pywin32</code> — for Windows GUI interaction (minimizing IDM window)</li>
    </ul>
  </li>
</ul>

<h2>Installation</h2>

<h3>1. Install Python</h3>
<ul>
  <li>Download and install Python 3.6 or later from <a href="https://www.python.org/">python.org</a></li>
  <li>During installation, check <strong>Add Python to PATH</strong></li>
  <li>Verify installation by opening a new terminal and running:<br>
    <code>python --version</code>
  </li>
</ul>

<h3>2. Install IDM</h3>
<ul>
  <li>Download and unzip IDM from the provided folder or official site</li>
  <li>Run the installer and follow the instructions</li>
  <li>Ensure IDM is running before starting downloads</li>
</ul>

<h3>3. Install Python dependencies</h3>
<p>Run the following command in your terminal or command prompt:</p>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>4. Install FFmpeg (required for merging video/audio formats)</h3>
<ul>
  <li>Visit <a href="https://ffmpeg.org/download.html">https://ffmpeg.org/download.html</a></li>
  <li>Download a Windows build (e.g., from gyan.dev or BtbN)</li>
  <li>Extract to a folder such as <code>C:\ffmpeg</code></li>
  <li>Add the <code>bin</code> directory to your system <code>PATH</code>:
    <ul>
      <li>Go to Windows Settings → System → About → Advanced system settings → Environment Variables</li>
      <li>Edit the <code>Path</code> variable and add <code>C:\ffmpeg\bin</code></li>
    </ul>
  </li>
  <li>Open a new terminal and verify installation by running:<br>
    <code>ffmpeg -version</code>
  </li>
</ul>

<h2>Usage</h2>
<p>Run the script:</p>
<pre><code>python ytdown.py</code></pre>

 
4. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt

## Contacts
-Telegram : https://t.me/Pilot2201
</br> -instagram
</br> -Email
