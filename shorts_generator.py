"""
100% FREE Automated YouTube Shorts / Reels / TikTok Generator
=============================================================
No paid AI subscriptions (no Flashloop needed!).
Generates vertical 9:16 (1080x1920) MP4 videos with:
1. Ultra-realistic Neural Voiceover (via free Microsoft Edge TTS)
2. Animated gradient / visual canvas + bold synced captions (via Pillow + MoviePy)

Quick Setup (run once in terminal):
    pip install edge-tts moviepy pillow numpy

Usage:
    python shorts_generator.py
"""

import asyncio
import math
import os
import textwrap
from pathlib import Path

import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# High-retention viral script presets (High-RPM niches: Finance, Psychology, Tech Facts)
SCRIPTS = [
    {
        "filename": "short_1_money_rule.mp4",
        "title": "THE 1% MONEY RULE",
        "segments": [
            "Why do ninety-nine percent of people stay broke even when their income goes up?",
            "It is called the Rat Race Trap.",
            "Every time most people get extra cash, they upgrade their lifestyle first.",
            "Wealthy people do the exact opposite.",
            "They buy or build one small income-producing asset before spending a single cent.",
            "Start building your digital assets today and follow for daily wealth rules."
        ],
    },
    {
        "filename": "short_2_psychology_pricing.mp4",
        "title": "PSYCHOLOGY OF SELLING",
        "segments": [
            "Never ask a business owner if they want to buy a website.",
            "If you ask first, they have to imagine it, and their brain defaults to saying no.",
            "Instead, show them a finished preview with their own business name already on it.",
            "This triggers the Endowment Effect.",
            "Once someone sees their name on something valuable, they do not want to lose it.",
            "Save this video and use this rule on your next pitch."
        ],
    },
]

VOICE = "en-US-ChristopherNeural"
W, H = 1080, 1920


async def generate_tts(text: str, out_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate="+8%")
    await communicate.save(out_path)


def render_caption_frame(title: str, caption: str, t: float) -> np.ndarray:
    """Renders a sleek 1080x1920 vertical frame with animated accent glow and bold captions."""
    img = Image.new("RGB", (W, H), (11, 13, 20))
    draw = ImageDraw.Draw(img)

    # Animated subtle glow circles
    cx = int(W / 2 + math.sin(t * 1.5) * 180)
    cy = int(H * 0.35 + math.cos(t * 1.2) * 120)
    for r in range(420, 40, -40):
        intensity = int((420 - r) * 0.12)
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(11 + intensity, 16 + int(intensity * 0.6), 28),
        )

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 52)
        font_body = ImageFont.truetype("arialbd.ttf", 72)
        font_footer = ImageFont.truetype("arial.ttf", 38)
    except OSError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # Top pill title
    draw.rounded_rectangle([140, 220, W - 140, 320], radius=50, fill=(245, 158, 11))
    draw.text((W // 2, 270), title, fill=(0, 0, 0), font=font_title, anchor="mm")

    # Center wrapped caption card
    lines = textwrap.wrap(caption.upper(), width=18)
    card_h = max(360, len(lines) * 95 + 120)
    top_y = (H - card_h) // 2
    draw.rounded_rectangle(
        [80, top_y, W - 80, top_y + card_h],
        radius=36,
        fill=(22, 27, 40),
        outline=(245, 158, 11),
        width=4,
    )

    y_text = top_y + 85
    for line in lines:
        draw.text((W // 2, y_text), line, fill=(255, 255, 255), font=font_body, anchor="mm")
        y_text += 95

    # Bottom hook bar
    draw.text(
        (W // 2, H - 220),
        ">> FOLLOW FOR DAILY WEALTH & TECH PLAYBOOKS <<",
        fill=(148, 163, 184),
        font=font_footer,
        anchor="mm",
    )
    return np.array(img)


async def build_short(item: dict, out_dir: Path):
    from moviepy import AudioFileClip, VideoClip, concatenate_videoclips

    temp_clips = []
    temp_audios = []

    print(f"\n[*] Building: {item['filename']} ...")
    for idx, seg_text in enumerate(item["segments"]):
        audio_file = out_dir / f"_temp_{idx}.mp3"
        await generate_tts(seg_text, str(audio_file))
        temp_audios.append(audio_file)

        audio_clip = AudioFileClip(str(audio_file))
        dur = audio_clip.duration

        def make_frame(t, text=seg_text, title=item["title"]):
            return render_caption_frame(title, text, t)

        v_clip = VideoClip(make_frame, duration=dur).with_audio(audio_clip)
        temp_clips.append(v_clip)

    final = concatenate_videoclips(temp_clips, method="compose")
    out_path = out_dir / item["filename"]
    final.write_videofile(str(out_path), fps=24, codec="libx264", audio_codec="aac", logger=None)

    for c in temp_clips:
        c.close()
    for a in temp_audios:
        if a.exists():
            os.remove(a)
    print(f"[+] Saved ready-to-upload Short: {out_path}")


async def main():
    out_dir = Path(__file__).parent / "generated_shorts"
    out_dir.mkdir(exist_ok=True)
    for item in SCRIPTS:
        await build_short(item, out_dir)


if __name__ == "__main__":
    asyncio.run(main())
