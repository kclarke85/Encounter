"""
seo_pitch_video.py

Generates an MP4 explainer video (with simple animations) for a SaaS SEO product.
This script:
 - Synthesizes narration audio for each script segment (uses pyttsx3 if available, falls back to gTTS).
 - Builds animated scene clips with MoviePy (text, simple shapes, "dashboard" mockups, map pins, PDF icon).
 - Syncs each scene to the duration of its narration.
 - Concatenates clips and writes seo_pitch.mp4

Dependencies:
    pip install moviepy pillow numpy pyttsx3 gTTS pydub

Notes:
 - pyttsx3 is offline and preferred. If it fails, gTTS (Google) will be used (requires internet).
 - On some systems, pyttsx3 may require additional voice/engine config (sapi5 on Windows, nsss on macOS).
 - If you want better-quality TTS (ElevenLabs, etc.) replace the synthesize_audio() implementation.
"""

import os
import math
import tempfile
from pathlib import Path
from typing import List, Tuple

from moviepy.editor import (
    TextClip, ImageClip, ColorClip, CompositeVideoClip,
    concatenate_videoclips, AudioFileClip, VideoFileClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ---- Optional TTS libs ----
try:
    import pyttsx3
    TTS_ENGINE = "pyttsx3"
except Exception:
    pyttsx3 = None
    try:
        from gtts import gTTS
        TTS_ENGINE = "gTTS"
    except Exception:
        TTS_ENGINE = None

# pydub for converting mp3->wav if needed
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except Exception:
    PYDUB_AVAILABLE = False

# --------------------------
# Configuration
# --------------------------
OUTPUT_FILE = "seo_pitch.mp4"
TMP_DIR = Path(tempfile.gettempdir()) / "seo_pitch_assets"
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Video specs
W, H = 1280, 720
FPS = 24
BG_COLOR = (245, 247, 250)  # soft light background

# Font settings (PIL & MoviePy)
# If you want a different font, set the path to a .ttf file available on your system
DEFAULT_FONT = None  # e.g., "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Voice settings
VOICE_RATE = 160  # words per minute (pyttsx3 uses a different scale; we attempt to set)
VOICE_VOLUME = 1.0

# --------------------------
# Script: list of (text, scene_type)
# scene_type informs the style of the scene we render.
# --------------------------
SCRIPT: List[Tuple[str, str]] = [
    ("Small businesses struggle to get noticed online. SEO is confusing, time-consuming, and often too expensive.", "problem"),
    ("That’s why we built our all-in-one SEO dashboard — a simple, powerful tool designed just for small businesses.", "intro"),
    ("Keyword research: discover the search terms and questions your customers are asking, powered by Google SERP API.", "keywords"),
    ("On-page SEO analysis: check titles, meta descriptions, H1 tags and image alt text, plus easy recommendations.", "onpage"),
    ("Backlink analysis: find who links to your competitors and spot opportunities to build authority.", "backlinks"),
    ("Local SEO tools: generate location-specific keywords and check your business listings across directories.", "local"),
    ("One-click PDF reports: compile findings into a professional downloadable report you can share.", "pdf"),
    ("Finally, SEO made simple. Get started today and take your small business to the top of Google.", "cta"),
]

# --------------------------
# Helper: text-to-speech
# Creates one audio file per script segment and returns list of file paths
# --------------------------
def synthesize_audio_segments(script: List[Tuple[str, str]], out_dir: Path) -> List[Path]:
    out_paths = []
    if TTS_ENGINE == "pyttsx3":
        print("Using pyttsx3 for offline TTS...")
        engine = pyttsx3.init()
        # Try to set voice rate and volume if supported
        try:
            engine.setProperty("rate", VOICE_RATE)
            engine.setProperty("volume", VOICE_VOLUME)
        except Exception:
            pass

        for i, (text, _) in enumerate(script):
            fname = out_dir / f"narr_{i}.wav"
            print(f"Synthesizing segment {i} -> {fname}")
            engine.save_to_file(text, str(fname))
        engine.runAndWait()

        # confirm files exist
        for i in range(len(script)):
            p = out_dir / f"narr_{i}.wav"
            if not p.exists():
                raise RuntimeError(f"TTS output missing: {p}")
            out_paths.append(p)

    elif TTS_ENGINE == "gTTS":
        print("pyttsx3 not available — falling back to gTTS (requires internet).")
        for i, (text, _) in enumerate(script):
            fname = out_dir / f"narr_{i}.mp3"
            print(f"Synthesizing segment {i} -> {fname}")
            tts = gTTS(text)
            tts.save(str(fname))
            # Convert mp3 -> wav for MoviePy consistency if pydub available
            if PYDUB_AVAILABLE:
                wav_name = out_dir / f"narr_{i}.wav"
                AudioSegment.from_mp3(str(fname)).export(str(wav_name), format="wav")
                out_paths.append(wav_name)
            else:
                out_paths.append(fname)
    else:
        raise RuntimeError("No TTS engine available. Install pyttsx3 or gTTS + pydub.")

    return out_paths

# --------------------------
# Scene generators
# Each takes a duration and returns a MoviePy clip sized W x H
# --------------------------
def make_text_slide(text: str, duration: float, title: str = None) -> CompositeVideoClip:
    """Simple centered text slide with fade-in/out animation."""
    fontsize = 42 if len(text) < 80 else 34
    txt_clip = TextClip(text, fontsize=fontsize, font=DEFAULT_FONT or "Arial-Bold", method="caption",
                        size=(W - 160, None), align="West")
    txt_clip = txt_clip.set_position(("center", "center")).set_duration(duration)
    # background
    bg = ColorClip(size=(W, H), color=BG_COLOR).set_duration(duration)
    # subtle entrance animation -> move from bottom slightly
    def pos(t):
        # simple ease-out
        start_y = H + 100
        end_y = H // 2
        frac = min(1, t / 0.6)
        y = start_y - (start_y - end_y) * (1 - (1 - frac) ** 3)
        return ("center", y)
    anim_txt = txt_clip.set_position(lambda t: pos(t))
    return CompositeVideoClip([bg, anim_txt]).set_duration(duration)

def make_dashboard_scene(duration: float) -> CompositeVideoClip:
    """Draw a multi-tab dashboard mockup. We'll produce animated tab highlights."""
    bg = ColorClip(size=(W, H), color=BG_COLOR).set_duration(duration)

    # Create a PIL image for a dashboard mockup
    im = Image.new("RGBA", (W - 200, H - 160), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    # simple header
    draw.rectangle([0, 0, im.width, 80], fill=(30, 58, 120))
    draw.text((20, 20), "SEO Dashboard", fill=(255, 255, 255), anchor=None)
    # tabs
    tab_w = 160
    tabs = ["Keywords", "On-Page", "Backlinks", "Local", "Reports"]
    for i, t in enumerate(tabs):
        x = 20 + i * (tab_w + 10)
        draw.rectangle([x, 100, x + tab_w, 140], outline=(200, 200, 200), width=2)
        draw.text((x + 10, 110), t, fill=(20, 20, 20))
    # a few rectangles to mimic lists and charts
    draw.rectangle([20, 160, im.width - 40, 320], outline=(220, 220, 220), width=2)
    draw.rectangle([20, 340, im.width - 40, im.height - 20], outline=(220, 220, 220), width=2)
    # small "chart" bars
    for i in range(6):
        bx = 40 + i * 90
        draw.rectangle([bx, 180, bx + 40, 300 - i * 10], fill=(100, 160, 240))
    pil_path = TMP_DIR / "dashboard_mock.png"
    im.save(pil_path)

    dash_clip = ImageClip(str(pil_path)).set_duration(duration).resize(width=W - 200).set_position(("center", "center"))

    # animate a highlight rectangle moving between tabs
    tab_positions = [ (100 + i*(tab_w+10), 170) for i in range(len(tabs)) ]
    # We'll use a small rectangle that moves across top area
    def moving_box(get_t):
        t=get_t
        # use time to index into tabs
        idx = min(len(tabs)-1, int((t / duration) * len(tabs)))
        # compute the x position to move smoothly
        frac = ((t / duration) * len(tabs)) - idx
        x0 = 100 + idx * (tab_w + 10)
        x1 = 100 + min(len(tabs)-1, idx+1) * (tab_w + 10)
        x = x0 + (x1 - x0) * frac
        return x

    # Create an animated rectangle using ColorClip and position lambda
    highlight = ColorClip(size=(tab_w, 38), color=(240, 244, 255)).with_duration(duration)
    highlight = highlight.set_position(lambda t: (moving_box(t), 150)).set_opacity(0.9)

    return CompositeVideoClip([bg, dash_clip, highlight]).set_duration(duration)

def make_keywords_scene(keywords_sample: List[str], duration: float) -> CompositeVideoClip:
    bg = ColorClip((W, H), color=BG_COLOR).set_duration(duration)
    title = TextClip("Keyword Research", fontsize=56, font=DEFAULT_FONT or "Arial-Bold").set_position((60, 40)).set_duration(duration)
    # create list items that animate in
    item_clips = []
    y0 = 130
    for i, kw in enumerate(keywords_sample[:6]):
        tstart = 0.3 + i * 0.35
        dur = max(1.5, duration - tstart)
        txt = TextClip(f"• {kw}", fontsize=38, font=DEFAULT_FONT or "Arial", method="label").set_duration(dur)
        txt = txt.set_position(("left", y0 + i * 60)).set_start(tstart)
        item_clips.append(txt)
    return CompositeVideoClip([bg, title, *item_clips]).set_duration(duration)

def make_onpage_scene(duration: float) -> CompositeVideoClip:
    bg = ColorClip((W, H), color=BG_COLOR).set_duration(duration)
    title = TextClip("On-Page SEO Analysis", fontsize=56, font=DEFAULT_FONT or "Arial-Bold").set_position((60, 40)).set_duration(duration)

    # Mock page screenshot rectangle
    page = ColorClip((700, 360), color=(255, 255, 255)).set_duration(duration).set_position((60, 120)).with_border(2, color=(220,220,220))
    # overlay some lines simulating meta and checks
    checks = []
    items = [
        ("Title tag", False),
        ("Meta description", False),
        ("H1 tags", True),
        ("Images with alt text", False),
        ("Page speed", True)
    ]
    for i, (name, ok) in enumerate(items):
        color = (34, 197, 94) if ok else (239, 68, 68)
        dot = ColorClip((18, 18), color=color).set_duration(duration).set_position((800, 150 + i * 40))
        txt = TextClip(f"{name}", fontsize=36, font=DEFAULT_FONT or "Arial").set_duration(duration).set_position((830, 140 + i * 40))
        checks.extend([dot, txt])
    return CompositeVideoClip([bg, title, page, *checks]).set_duration(duration)

def make_backlinks_scene(duration: float) -> CompositeVideoClip:
    bg = ColorClip((W, H), color=BG_COLOR).set_duration(duration)
    title = TextClip("Backlink Opportunities", fontsize=56, font=DEFAULT_FONT or "Arial-Bold").set_position((60, 40)).set_duration(duration)

    # Draw several small website boxes at left and arrows to a central target site
    boxes = []
    for i in range(6):
        x = 80
        y = 120 + i * 70
        box = ColorClip((260, 50), color=(255, 255, 255)).set_duration(duration).set_position((x, y)).with_border = None
        txt = TextClip(f"site{i+1}.com", fontsize=28).set_duration(duration).set_position((x + 10, y + 10))
        # arrow: we simulate by a long thin rectangle moving from box to center
        arrow = ColorClip((300, 4), color=(100, 120, 200)).set_duration(duration).set_position((x + 260, y + 22)).rotate(0)
        boxes.extend([box, txt, arrow])
    central = ColorClip((320, 120), color=(255, 255, 255)).set_duration(duration).set_position((700, 200))
    central_txt = TextClip("yourbusiness.com", fontsize=36).set_duration(duration).set_position((720, 250))
    return CompositeVideoClip([bg, title, *boxes, central, central_txt]).set_duration(duration)

def make_local_scene(duration: float) -> CompositeVideoClip:
    bg = ColorClip((W, H), color=BG_COLOR).set_duration(duration)
    title = TextClip("Local SEO Tools", fontsize=56, font=DEFAULT_FONT or "Arial-Bold").set_position((60, 40)).set_duration(duration)

    # simple map illustration (colored rectangle) with pins
    map_clip = ColorClip((760, 420), color=(230, 240, 250)).set_duration(duration).set_position((60, 120))
    pins = []
    pin_positions = [(180, 200), (380, 260), (420, 180), (620, 300)]
    for i, (px, py) in enumerate(pin_positions):
        circ = ColorClip((18, 18), color=(220, 36, 36)).set_duration(duration).set_position((px, py))
        label = TextClip(f"Plumber {['NY','LA','TX','FL'][i]}", fontsize=28).set_duration(duration).set_position((px+24, py-6))
        pins.extend([circ, label])
    return CompositeVideoClip([bg, title, map_clip, *pins]).set_duration(duration)

def make_pdf_scene(duration: float) -> CompositeVideoClip:
    bg = ColorClip((W, H), color=BG_COLOR).set_duration(duration)
    title = TextClip("Shareable PDF Reports", fontsize=56, font=DEFAULT_FONT or "Arial-Bold").set_position((60, 40)).set_duration(duration)
    # create a faux PDF paper that slides in, then a download icon
    paper = ColorClip((520, 680), color=(255,255,255)).set_duration(duration).set_position((W, H//2)).resize(width=420)
    paper = paper.set_position(lambda t: (W//2 - 200, H + (H//2 - 80) * (1 - t / max(0.8, duration))))  # slide-up entrance
    stamp = TextClip("PDF", fontsize=80, font=DEFAULT_FONT or "Arial-Bold").set_duration(duration).set_position((W//2+80, H//2-60)).set_opacity(0.9)
    return CompositeVideoClip([bg, title, paper, stamp]).set_duration(duration)

def make_cta_scene(duration: float) -> CompositeVideoClip:
    bg = ColorClip((W, H), color=(20, 60, 120)).set_duration(duration)
    big = TextClip("SEO made simple.", fontsize=72, color="white", font=DEFAULT_FONT or "Arial-Bold").set_position(("center", H//2 - 30)).set_duration(duration)
    sub = TextClip("Get started today. Visit: yourproduct.example", fontsize=36, color="white", font=DEFAULT_FONT or "Arial").set_position(("center", H//2 + 50)).set_duration(duration)
    return CompositeVideoClip([bg, big, sub]).set_duration(duration)

# Map scene type to generator
SCENE_GENERATORS = {
    "problem": make_text_slide,
    "intro": make_dashboard_scene,
    "keywords": lambda duration, **kw: make_keywords_scene(
        ["plumber near me", "emergency plumber", "how much does a plumber cost", "best plumber NYC", "plumber reviews", "plumbing services"], duration),
    "onpage": make_onpage_scene,
    "backlinks": make_backlinks_scene,
    "local": make_local_scene,
    "pdf": make_pdf_scene,
    "cta": make_cta_scene,
}

# --------------------------
# Main assembly
# --------------------------
def build_video(script: List[Tuple[str, str]], out_path: str):
    print("Synthesizing audio...")
    aud_files = synthesize_audio_segments(script, TMP_DIR)

    clips = []
    print("Building scenes...")
    for i, ((text, scene_type), aud_fp) in enumerate(zip(script, aud_files)):
        # load audio to get duration
        audio_clip = AudioFileClip(str(aud_fp))
        duration = audio_clip.duration + 0.25  # small pad for visuals
        print(f"Scene {i} ({scene_type}): duration {duration:.2f}s")

        # select generator
        gen = SCENE_GENERATORS.get(scene_type, None)
        if gen is None:
            # fallback to text slide
            scene = make_text_slide(text, duration)
        else:
            # many generators accept duration only; some have custom signatures
            try:
                scene = gen(duration)
                # if generator returned a TextClip instead, wrap it
                if isinstance(scene, TextClip):
                    scene = CompositeVideoClip([ColorClip((W,H), BG_COLOR).set_duration(duration), scene.set_duration(duration)])
            except TypeError:
                # maybe the generator expects text as first argument
                scene = gen(text, duration)

        # Attach audio
        scene = scene.set_audio(audio_clip)
        # Ensure proper size
        scene = scene.set_fps(FPS).resize((W, H))
        clips.append(scene)

    print("Concatenating clips...")
    final = concatenate_videoclips(clips, method="compose")
    # Add a short outro silence if needed
    print(f"Writing final video to {out_path} ... this may take a minute.")
    final.write_videofile(out_path, fps=FPS, codec="libx264", audio_codec="aac", preset="medium", threads=4)
    print("Done.")

# --------------------------
# Utility: cleanup temp assets (optional)
# --------------------------
def cleanup_temp():
    for f in TMP_DIR.glob("narr_*"):
        try:
            f.unlink()
        except Exception:
            pass

# --------------------------
# Entry point
# --------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate an explainer MP4 for a SaaS SEO product.")
    parser.add_argument("--out", type=str, default=OUTPUT_FILE, help="Output MP4 filename")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary audio assets")
    args = parser.parse_args()

    try:
        build_video(SCRIPT, args.out)
    finally:
        if not args.keep_temp:
            cleanup_temp()
