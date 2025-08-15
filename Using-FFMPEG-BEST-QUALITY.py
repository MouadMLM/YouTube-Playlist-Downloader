
"""
Optimized YouTube Playlist Downloader (yt-dlp 2025 Edition)
Author: Mouadev (Improved & Hardened)

Features:
- Multi-threaded video downloads
- Automatic retries for failed videos
- Smart format fallback (1080p preferred)
- Skips already downloaded videos
- Handles YouTube throttling issues
"""

import os
import re
import time
import yt_dlp
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class StrongDownloader:
    def _init_(self):
        self.downloaded = 0
        self.skipped = 0
        self.failed = 0
        self.total = 0
        self.lock = threading.Lock()

    @staticmethod
    def sanitize_title(title: str) -> str:
        invalid = r'<>:"/\\|?*'
        for ch in invalid:
            title = title.replace(ch, "")
        title = re.sub(r"\s+", " ", title).strip()
        return title[:150]

    @staticmethod
    def clean_url(url: str) -> str:
        match = re.search(r"list=([a-zA-Z0-9_-]+)", url)
        return f"https://www.youtube.com/playlist?list={match.group(1)}" if match else url

    def get_existing_files(self, path):
        exts = {".mp4", ".webm", ".mkv", ".avi", ".mov", ".flv", ".m4v"}
        return {os.path.splitext(f)[0].lower() for f in os.listdir(path) if os.path.splitext(f)[1].lower() in exts}

    def get_playlist(self, url):
        opts = {
            "extract_flat": True,
            "quiet": True,
            "ignoreerrors": True
        }
        for attempt in range(3):
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("No info extracted")
                entries = [e for e in info.get("entries", []) if e]
                return info.get("title", "Unknown Playlist"), entries
            except Exception as e:
                print(f"⚠ Playlist extraction failed ({attempt+1}/3): {e}")
                time.sleep(2)
        return None, []

    def download_video(self, video, save_path, existing, thread_id):
        vid_id = video.get("id", "")
        title = self.sanitize_title(video.get("title", f"video_{vid_id}"))

        if title.lower() in existing:
            with self.lock:
                self.skipped += 1
                print(f"⏭ [T{thread_id}] Skipped: {title}")
            return

        url = f"https://www.youtube.com/watch?v={vid_id}"
        formats = [
            "bestvideo[height<=1080]+bestaudio[ext=m4a]/best[height<=1080]",
            "best[ext=mp4]",
            "best"
        ]

        for fmt in formats:
            opts = {
                "format": fmt,
                "outtmpl": os.path.join(save_path, f"{title}.%(ext)s"),
                "merge_output_format": "mp4",
                "quiet": True,
                "ignoreerrors": False,
                "retries": 5,
                "throttled_rate": 0,  # helps bypass throttling
            }
            try:
                with self.lock:
                    print(f"⬇ [T{thread_id}] Downloading: {title[:60]}")
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                with self.lock:
                    self.downloaded += 1
                    print(f"✅ [T{thread_id}] Done: {title}")
                return
            except Exception as e:
                if "requested format not available" in str(e).lower():
                    continue
                error_msg = str(e).split("\n")[0][:70]
                with self.lock:
                    print(f"⚠ [T{thread_id}] Retry: {title} ({error_msg})")
        with self.lock:
            self.failed += 1
            print(f"❌ [T{thread_id}] Failed: {title}")

    def run(self, url, workers=4):
        url = self.clean_url(url)
        name, videos = self.get_playlist(url)
        if not videos:
            print("❌ No videos found.")
            return
        self.total = len(videos)

        folder = self.sanitize_title(name)[:50] or "youtube_playlist"
        save_path = os.path.join(str(Path.home() / "Downloads"), folder)
        os.makedirs(save_path, exist_ok=True)
        existing = self.get_existing_files(save_path)

        print(f"📋 Playlist: {name}")
        print(f"📹 Total: {self.total} | Already: {len(existing)}")
        print(f"📁 Save to: {save_path}")
        print(f"🚀 Starting {workers} threads...\n")

        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(self.download_video, v, save_path, existing, i % workers + 1)
                       for i, v in enumerate(videos)]
            for f in as_completed(futures):
                pass

        end = time.time()
        print("\n" + "="*50)
        print(f"✅ Downloaded: {self.downloaded}")
        print(f"⏭ Skipped: {self.skipped}")
        print(f"❌ Failed: {self.failed}")
        print(f"⏱ Time: {round(end - start, 1)}s")
        print("="*50)


if _name_ == "_main_":
    print("🎵 STRONG YOUTUBE PLAYLIST DOWNLOADER")
    url = input("Enter YouTube playlist/video URL: ").strip()
    workers = input("Threads (default 4, max 8): ").strip()
    try:
        workers = min(int(workers), 8) if workers else 4
    except:
        workers = 4
    StrongDownloader().run(url, workers)
