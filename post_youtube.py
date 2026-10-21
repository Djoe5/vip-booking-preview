import os
import sys
import webbrowser
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent
SHORTS_DIR = ROOT_DIR / "generated_shorts"

YOUTUBE_STUDIO_UPLOAD_URL = "https://studio.youtube.com/channel/UChmWzm_PIs3AiW3E9R6cT7g/videos/upload?d=pt"

DEFAULT_VIDEO = "short_kinetic_gta_ai_cashflow.mp4"

def main():
    target_video_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VIDEO
    target_path = SHORTS_DIR / target_video_name
    
    if not target_path.exists():
        target_path = ROOT_DIR / target_video_name

    print(f"[*] Preparing YouTube Studio upload for: {target_video_name}")
    print(f"[*] Opening YouTube Studio upload modal in your browser...")
    webbrowser.open(YOUTUBE_STUDIO_UPLOAD_URL)
    
    if target_path.exists():
        print(f"[*] Highlighting video file in Windows Explorer for instant drag-and-drop: {target_path}")
        subprocess.run(["explorer.exe", f"/select,{str(target_path)}"])
    else:
        print(f"[!] Warning: Video file {target_video_name} not found locally.")

    print("\n[+] YouTube Studio is open! Simply drag the highlighted video into the upload box and hit Publish!")

if __name__ == "__main__":
    main()
