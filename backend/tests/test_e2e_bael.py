"""
Standalone end-to-end test for the v2 render pipeline on the `bael` sample.

Run (from repo root):
  env -u PYTHONPATH backend/.venv/Scripts/python.exe tests/test_e2e_bael.py

It:
  1. Transcribes the voice (whisper, uses cached model)
  2. Generates captions (ASS)
  3. Builds a scene/section-aware timeline
  4. Loads brand config
  5. Renders output.mp4 with logo + captions + ken burns
  6. Verifies the output with ffprobe
"""
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # repo root
sys.path.insert(0, str(ROOT / "backend"))

from app.services.voice_service import voice_service
from app.services.caption_service import caption_service
from app.services.timeline_engine import timeline_engine
from app.services.brand_service import brand_service
from app.services.render_service import render_service
from app.services.script_service import script_service


def main():
    project_id = "bael"
    project_path = ROOT / "projects" / project_id

    voice_dir = project_path / "voice"
    audio_files = [f for f in voice_dir.iterdir() if f.is_file()]
    assert audio_files, "No voice file"
    audio_path = str(voice_dir / audio_files[0])

    # script
    script_text = ""
    script_dir = project_path / "script"
    if (script_dir / "script.txt").exists():
        script_text = (script_dir / "script.txt").read_text(encoding="utf-8")

    print("[1/5] Transcribing voice (whisper)...")
    word_timings = voice_service.transcribe_voice(audio_path, script_text=script_text)
    print(f"      -> {len(word_timings)} word timings, "
          f"total {word_timings[-1]['end']:.1f}s")

    print("[2/5] Parsing script sections...")
    sections = script_service.parse_script(script_text)
    print(f"      -> sections: {[s['name'] for s in sections]}")

    print("[3/5] Generating captions (ASS)...")
    subtitle_path = str(project_path / "temp" / "captions.ass")
    caption_service.generate_ass_file(word_timings, subtitle_path)
    print(f"      -> wrote {subtitle_path}")

    print("[4/5] Building scene-aware timeline...")
    brand = brand_service.load(project_path)
    timeline = timeline_engine.generate_timeline(
        project_path, word_timings, script_text=script_text
    )
    print(f"      -> {len(timeline)} clips")
    for c in timeline:
        print(f"         {c['scene']:10s} {c['media_type']:5s} "
              f"{c['start']:6.2f}-{c['end']:6.2f}s  {c['media']}")
    print(f"      -> brand: logo={bool(brand['logo'])} "
          f"music={bool(brand['music'])}")

    print("[5/5] Rendering output.mp4 (logo + captions + ken burns)...")
    out = render_service.render(
        project_path, timeline, audio_path, subtitle_path, brand=brand
    )
    print(f"      -> rendered: {out}")

    # Verify
    import subprocess
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,codec_name,width,height",
         "-of", "default=noprint_wrappers=1", out],
        capture_output=True, text=True,
    )
    print("\n[VERIFY] ffprobe output:")
    print(r.stdout or r.stderr)
    print("\nDONE.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
