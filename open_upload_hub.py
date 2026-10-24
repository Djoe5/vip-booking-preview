"""
One-Click Upload Hub Launcher for Today's Batch (October 22, 2026)
Opens TikTok Upload, YouTube Studio, and highlights today's 3 video files in Explorer.
"""
import subprocess
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent

TIKTOK_UPLOAD = "https://www.tiktok.com/upload"
YOUTUBE_UPLOAD = "https://studio.youtube.com/channel/UChmWzm_PIs3AiW3E9R6cT7g/videos/upload?d=pt"
INSTAGRAM_CREATE = "https://www.instagram.com/"

def main():
    print("[*] Opening TikTok Creator Upload...")
    webbrowser.open(TIKTOK_UPLOAD)
    
    print("[*] Opening YouTube Studio Upload...")
    webbrowser.open(YOUTUBE_UPLOAD)
    
    print("[*] Opening Instagram Web...")
    webbrowser.open(INSTAGRAM_CREATE)
    
    # Highlight the first video file in Explorer
    video_1 = ROOT / "short_kinetic_gta_silent_wealth.mp4"
    if video_1.exists():
        print(f"[*] Opening folder and selecting video: {video_1.name}")
        subprocess.run(["explorer.exe", f"/select,{str(video_1)}"])

if __name__ == "__main__":
    main()
