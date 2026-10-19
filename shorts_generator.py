"""
100% FREE Kinetic Subtitle Shorts Generator (V3.0 - Hormozi / CapCut Style)
===========================================================================
- ZERO alert frames, ZERO boxes.
- Real 60FPS vertical GTA 5 car mega ramp gameplay.
- REAL-TIME WORD-BY-WORD SYNCHRONIZATION:
  * Only displays 1 to 2 words at a time as they are spoken.
  * Active spoken word flashes in NEON GREEN (#00FF66) / ELECTRIC YELLOW (#FFE000).
  * 115pt ultra-bold Impact font with 14px black outline.
"""

import asyncio
import os
import re
from pathlib import Path

import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SCRIPTS = [
    {
        "filename": "short_kinetic_gta_money_glitch.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "HOW TO ESCAPE THE RAT RACE",
        "sentences": [
            "Stop working forty hours a week just to stay broke.",
            "The secret of the rich is building digital assets.",
            "Local businesses in Nairobi will gladly pay you fifty dollars for a website.",
            "You can build it in fifteen minutes with zero code.",
            "One client every two days is over one hundred thousand shillings a month.",
            "Check the link in bio to start right now."
        ],
    },
    {
        "filename": "short_kinetic_gta_dopamine_reset.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "THE 24-HOUR RESET",
        "sentences": [
            "Your attention span has been completely destroyed by short form content.",
            "Every time you swipe, your brain gets a cheap hit of dopamine.",
            "To fix this, go twenty-four hours without social media or sugar.",
            "Your focus will instantly return to superhuman levels.",
            "Follow The Mind Glitch and save this video."
        ],
    }
]

VOICE = "en-US-ChristopherNeural"
W, H = 1080, 1920
ROOT_DIR = Path(__file__).parent


async def generate_tts(text: str, out_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate="+12%")
    await communicate.save(out_path)


def get_font(size: int):
    paths = [
        r"C:\Windows\Fonts\impact.ttf",
        r"C:\Windows\Fonts\ariblk.ttf",
        r"C:\Windows\Fonts\arialbd.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def render_kinetic_frame(bg_frame: np.ndarray, title: str, words: list, word_idx: int) -> np.ndarray:
    """
    Renders ONLY the active 1-2 words currently spoken.
    Massive 115pt font, heavy 14px black outline, neon green highlight, floating seamlessly.
    """
    img = Image.fromarray(bg_frame).convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_title = get_font(52)
    font_word = get_font(115)
    font_sub = get_font(38)

    # Floating top title in electric yellow (no box)
    draw.text(
        (W // 2, 220),
        title.upper(),
        fill=(255, 230, 0),
        font=font_title,
        anchor="mm",
        stroke_width=8,
        stroke_fill=(0, 0, 0),
    )

    # Word-by-word active chunk (1 to 2 words max)
    if words:
        curr_word = words[min(word_idx, len(words) - 1)].upper()
        # Clean punctuation for display
        clean_word = re.sub(r'[^A-Z0-9$]', '', curr_word)

        # Alternating neon green and electric yellow for punch
        neon_color = (0, 255, 102) if (word_idx % 2 == 0) else (255, 230, 0)

        # Floating active word in center-lower third
        draw.text(
            (W // 2, 1140),
            clean_word,
            fill=neon_color,
            font=font_word,
            anchor="mm",
            stroke_width=14,
            stroke_fill=(0, 0, 0),
        )

    # Floating bottom brand watermark
    draw.text(
        (W // 2, H - 220),
        ">> THE MIND GLITCH <<",
        fill=(255, 255, 255),
        font=font_sub,
        anchor="mm",
        stroke_width=6,
        stroke_fill=(0, 0, 0),
    )

    return np.array(img.convert("RGB"))


async def build_short(item: dict, out_dir: Path):
    from moviepy import AudioFileClip, VideoClip, VideoFileClip, concatenate_videoclips

    bg_path = ROOT_DIR / item.get("bg_video", "gta_vertical.mp4")
    if not bg_path.exists():
        bg_path = ROOT_DIR / "gameplay_bg.mp4"

    bg_clip = VideoFileClip(str(bg_path))
    temp_clips = []
    temp_audios = []

    print(f"\n[*] Rendering: {item['filename']} with Real-Time Word-By-Word Kinetic Subtitles...")
    t_pointer = 8.0 # Start 8 seconds in where the car ramp action is intense

    for idx, sentence in enumerate(item["sentences"]):
        audio_file = out_dir / f"_temp_{idx}.mp3"
        await generate_tts(sentence, str(audio_file))
        temp_audios.append(audio_file)

        audio_clip = AudioFileClip(str(audio_file))
        dur = audio_clip.duration

        words = sentence.strip().split()
        num_words = max(1, len(words))
        word_dur = dur / num_words
        seg_start_t = t_pointer

        def make_frame(t, w_list=words, w_dur=word_dur, title=item["title"], start_t=seg_start_t):
            bg_time = (start_t + t) % bg_clip.duration
            bg_frame = bg_clip.get_frame(bg_time)
            curr_idx = min(int(t / w_dur), len(w_list) - 1)
            return render_kinetic_frame(bg_frame, title, w_list, curr_idx)

        v_clip = VideoClip(make_frame, duration=dur).with_audio(audio_clip)
        temp_clips.append(v_clip)
        t_pointer += dur

    final = concatenate_videoclips(temp_clips, method="compose")
    out_path = out_dir / item["filename"]
    final.write_videofile(
        str(out_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None,
    )

    for c in temp_clips:
        c.close()
    for a in temp_audios:
        if a.exists():
            os.remove(a)
    bg_clip.close()

    print(f"[+] Saved ready-to-upload Short: {out_path}")


async def main():
    out_dir = ROOT_DIR / "generated_shorts"
    out_dir.mkdir(exist_ok=True)
    for item in SCRIPTS:
        await build_short(item, out_dir)


if __name__ == "__main__":
    asyncio.run(main())
