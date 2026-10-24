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
    },
    {
        "filename": "short_kinetic_gta_dark_psychology.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "THE DARK PSYCHOLOGY RULE",
        "sentences": [
            "Most people fail because they wait for motivation.",
            "Motivation is a chemical trap that disappears in five minutes.",
            "The top one percent build systems that execute regardless of emotions.",
            "If you do not build your own dream, someone will hire you to build theirs.",
            "Follow The Mind Glitch and master your psychology."
        ],
    },
    {
        "filename": "short_kinetic_gta_ai_cashflow.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "THE 2026 AI CASHFLOW",
        "sentences": [
            "Ninety-nine percent of people use AI to write funny jokes.",
            "The smart one percent use AI to build daily cash machines.",
            "Local businesses will gladly pay you fifty dollars for a one-click website.",
            "You can deploy the entire site in ten minutes for zero dollars.",
            "Check the link in bio to grab the exact playbook."
        ],
    },
    {
        "filename": "short_kinetic_gta_silent_wealth.mp4",
        "bg_video": "gameplay_bg.mp4",
        "title": "RULE OF SILENT WEALTH",
        "sentences": [
            "Never announce your goals before you execute them.",
            "When you talk about your plans, your brain gets fake satisfaction.",
            "Work in complete silence and let your bank balance make the noise.",
            "Stack digital assets every single day while the crowd stays distracted.",
            "Follow The Mind Glitch for daily wealth rules."
        ],
    },
    {
        "filename": "short_kinetic_gta_dopamine_trap.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "THE DOPAMINE TRAP",
        "sentences": [
            "Your phone is designed to steal your focus and keep you broke.",
            "Every infinite scroll floods your brain with cheap dopamine.",
            "The top performers protect their attention like gold.",
            "Cut the noise, master your craft, and build daily income streams.",
            "Follow The Mind Glitch to take back your mind."
        ],
    },
    {
        "filename": "short_kinetic_gta_money_machine.mp4",
        "bg_video": "gameplay_bg.mp4",
        "title": "THE 100-DOLLAR GLITCH",
        "sentences": [
            "Here is how to make your first one hundred dollars online.",
            "Find five local business owners who have no website.",
            "Offer them a clean modern booking page in twenty-four hours.",
            "Charge fifty dollars each and use free AI templates.",
            "Check the link in bio to copy my exact framework."
        ],
    },
    {
        "filename": "short_kinetic_gta_7_second_rule.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "THE 7-SECOND RULE",
        "sentences": [
            "Your brain has a seven second window before it kills your ambition.",
            "The moment you have an instinct to act, count down seven seconds and move.",
            "If you hesitate, your mind creates fear and excuses to keep you safe.",
            "High performers do not wait to feel ready, they execute immediately.",
            "Follow The Mind Glitch and master your mental discipline."
        ],
    },
    {
        "filename": "short_kinetic_gta_digital_monopoly.mp4",
        "bg_video": "gameplay_bg.mp4",
        "title": "THE DIGITAL MONOPOLY",
        "sentences": [
            "Ten-person agencies are getting completely replaced by solo creators.",
            "One person using free AI tools can deliver websites in twenty minutes.",
            "Charge fifty dollars per client and take five clients a week.",
            "That is over one hundred and thirty thousand shillings pure profit every month.",
            "Check the link in bio to copy the exact automated setup."
        ],
    },
    {
        "filename": "short_kinetic_gta_silent_moves.mp4",
        "bg_video": "gta_vertical.mp4",
        "title": "NEVER REVEAL YOUR CARDS",
        "sentences": [
            "The biggest mistake broke people make is seeking validation.",
            "They post their goals, brag about their plans, and end up achieving nothing.",
            "Move in total stealth until the results are too loud to ignore.",
            "Stack cash, build systems, and let your silence do the talking.",
            "Follow The Mind Glitch and protect your energy."
        ],
    }
]

VOICE = "en-US-ChristopherNeural"
W, H = 1080, 1920
ROOT_DIR = Path(__file__).parent


async def generate_tts(text: str, out_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate="+12%")
    await communicate.save(out_path)


from functools import lru_cache

@lru_cache(maxsize=16)
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


EMOJI_MAP = {
    "MONEY": " 💸", "DOLLARS": " 💵", "SHILLINGS": " 💰", "CASH": " 🤑",
    "BRAIN": " 🧠", "ATTENTION": " 🎯", "DOPAMINE": " ⚡", "FOCUS": " 👁️",
    "RULES": " 📜", "SECRET": " 🤫", "TRAP": " 🪤", "LIE": " ⚠️",
    "STOP": " 🛑", "FAIL": " ❌", "FREE": " 🔓", "RICH": " 👑",
    "AI": " 🤖", "DIGITAL": " 💻", "SYSTEMS": " ⚙️", "CLIENT": " 🤝",
    "HOURS": " ⏳", "RESET": " 🔄", "FREEDOM": " 🚀", "SECONDS": " ⏱️",
    "SILENCE": " 🤫", "DISCIPLINE": " 🛡️", "ENERGY": " ⚡", "CARDS": " 🃏",
    "FEAR": " 🥶", "POWER": " ⚡", "PROFIT": " 📈", "ACTION": " 🚀"
}

PALETTES = [
    (0, 255, 102),   # Neon Green
    (0, 245, 255),   # Cyber Cyan
    (255, 230, 0),   # Electric Gold
    (255, 50, 150),  # Hot Magenta
]

def render_kinetic_frame(bg_frame: np.ndarray, title: str, words: list, word_idx: int, progress: float = 0.0) -> np.ndarray:
    """
    Renders ONLY the active 1-2 words currently spoken.
    Massive 115pt font, heavy 14px black outline, dynamic neon color, contextual emojis,
    and a sleek animated progress bar.
    """
    img = Image.fromarray(bg_frame).convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_title = get_font(52)
    font_word = get_font(110)
    font_sub = get_font(38)

    # Sleek animated top progress bar (boosts watch completion)
    bar_width = int(W * max(0.0, min(1.0, progress)))
    if bar_width > 0:
        draw.rectangle([(0, 0), (bar_width, 10)], fill=(0, 245, 255, 230))

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

    # Word-by-word active chunk
    if words:
        curr_word = words[min(word_idx, len(words) - 1)].upper()
        clean_word = re.sub(r'[^A-Z0-9$]', '', curr_word)
        
        # Attach high-energy contextual emoji if recognized
        emoji = EMOJI_MAP.get(clean_word, "")
        display_text = clean_word + emoji

        # Dynamic cycling neon color
        neon_color = PALETTES[word_idx % len(PALETTES)]

        # Floating active word in center-lower third
        draw.text(
            (W // 2, 1140),
            display_text,
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

    print(f"\n[*] Rendering: {item['filename']} with Real-Time Word-By-Word Kinetic Subtitles...", flush=True)
    t_pointer = 8.0 # Start 8 seconds in where the car ramp action is intense

    for idx, sentence in enumerate(item["sentences"]):
        audio_file = out_dir / f"_temp_{idx}.mp3"
        await generate_tts(sentence, str(audio_file))
        temp_audios.append(audio_file)
        print(f"  [+] TTS chunk {idx+1}/{len(item['sentences'])} done", flush=True)

        audio_clip = AudioFileClip(str(audio_file))
        dur = audio_clip.duration

        words = sentence.strip().split()
        num_words = max(1, len(words))
        word_dur = dur / num_words
        seg_start_t = t_pointer
        elapsed_before = t_pointer - 8.0

        def make_frame(t, w_list=words, w_dur=word_dur, title=item["title"], start_t=seg_start_t, el_before=elapsed_before):
            bg_time = (start_t + t) % bg_clip.duration
            bg_frame = bg_clip.get_frame(bg_time)
            curr_idx = min(int(t / w_dur), len(w_list) - 1)
            # Rough 20s total estimate for progress bar
            progress = min(1.0, (el_before + t) / 22.0)
            return render_kinetic_frame(bg_frame, title, w_list, curr_idx, progress=progress)

        v_clip = VideoClip(make_frame, duration=dur).with_audio(audio_clip)
        temp_clips.append(v_clip)
        t_pointer += dur

    print(f"  [+] Concatenating and encoding {item['filename']}...", flush=True)
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

    print(f"[+] Saved ready-to-upload Short: {out_path}", flush=True)


import sys

async def main():
    out_dir = ROOT_DIR / "generated_shorts"
    out_dir.mkdir(exist_ok=True)
    
    target_scripts = SCRIPTS
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        idx = int(sys.argv[1])
        if 0 <= idx < len(SCRIPTS):
            target_scripts = [SCRIPTS[idx]]
        else:
            print(f"[!] Invalid index {idx}. Available: 0 to {len(SCRIPTS)-1}")
            return

    for item in target_scripts:
        out_path = out_dir / item["filename"]
        if out_path.exists() and "--force" not in sys.argv:
            print(f"[*] Skipping {item['filename']} (already exists). Use --force to re-render.", flush=True)
            continue
        print(f"\n[>] Rendering: {item['title']} -> {item['filename']}", flush=True)
        await build_short(item, out_dir)

if __name__ == "__main__":
    asyncio.run(main())
