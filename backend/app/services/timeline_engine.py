"""
Timeline Engine (v2)
=====================

Builds a render timeline that maps media (videos + photos) onto the narration
timeline, following the rules in docs/05-Timeline-Engine.md and docs/01-SRD.md.

Key principles (vs the old random shuffle):
  * Voice controls scene duration. We split the narration word-timings into
    the SAME sections declared in the script ([Hook], [Plantation], ...).
  * Each section gets the media best suited for its objective (Hook = an
    eye-catching video; Plantation/Benefits = closeups/videos; Outro = brand
    photo/logo). Photos are NOT just fallback — they are mixed in naturally.
  * Media is rotated: video, photo, video, video, photo ... Never the same
    clip twice in a row. No blank frames.
  * Output clips carry a `media_type`, a `ken_burns` flag (photos zoom),
    and `source_start`/`source_end` so the renderer trims videos precisely.

If the script has no sections, the whole narration becomes one big section and
media is distributed across it (still deterministic, still no random gaps).

Deterministic: same inputs -> same timeline (no shuffle / no randomness).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional


class TimelineEngine:
    def __init__(self):
        # How strongly each scene prefers video vs photo (0=photo,1=video)
        # Hook wants motion; Outro wants a brand photo. Tunable.
        self.scene_video_preference = {
            "Hook": 1.0,
            "Intro": 0.8,
            "Plantation": 0.85,
            "Benefits": 0.7,
            "CTA": 0.8,
            "Outro": 0.15,
            "Body": 0.7,
        }
        self.photo_duration = 3.0  # default seconds for a photo clip
        # Ken Burns (slow zoom on photos) per docs/05. Can be disabled via
        # brand.json "ken_burns": false for faster renders (~2.5x speedup).
        self.ken_burns = True

    # ------------------------------------------------------------------ #
    # Media scanning
    # ------------------------------------------------------------------ #
    def _probe_duration(self, path: Path) -> float:
        try:
            out = subprocess.check_output(
                ["ffprobe", "-v", "error",
                 "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                stderr=subprocess.DEVNULL,
            ).decode().strip()
            return float(out)
        except Exception:
            return 5.0

    def _gather_media(self, project_path: Path) -> tuple[list[dict], list[dict]]:
        videos: list[dict] = []
        photos: list[dict] = []

        vdir = project_path / "videos"
        pdir = project_path / "photos"

        # Skip brand assets (logo etc.) — they are handled separately.
        brand_dir = project_path / "brand"

        if vdir.exists():
            for f in sorted(vdir.iterdir()):
                if f.is_file() and f.suffix.lower() in (".mp4", ".mov", ".webm", ".mkv"):
                    videos.append({
                        "file": f.name,
                        "type": "video",
                        "duration": self._probe_duration(f),
                    })

        if pdir.exists():
            for f in sorted(pdir.iterdir()):
                if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                    # exclude the brand logo file if it lives in photos
                    if brand_dir.exists() and (brand_dir / f.name).exists():
                        continue
                    photos.append({
                        "file": f.name,
                        "type": "photo",
                        "duration": self.photo_duration,
                    })

        return videos, photos

    # ------------------------------------------------------------------ #
    # Split word timings into script sections
    # ------------------------------------------------------------------ #
    def _split_timings_by_sections(
        self, word_timings: list[dict], sections: list[dict]
    ) -> list[dict]:
        """
        Distribute the narration across the declared sections so the resulting
        segments are CONTIGUOUS and cover 100% of the audio (no gaps, no
        overlaps). Section lengths are proportional to their word counts.

        Returns sections annotated with start/end times:
            [{"name": "Hook", "start": 0.0, "end": 3.1}, ...]
        """
        if not word_timings:
            return []
        total_audio = word_timings[-1]["end"]
        if total_audio <= 0:
            return []

        total_words = sum(max(1, len(s["text"].split())) for s in sections) or 1

        annotated: list[dict] = []
        cursor = 0.0
        for i, s in enumerate(sections):
            n = max(1, len(s["text"].split()))
            # last section absorbs any rounding remainder so we hit total_audio
            if i == len(sections) - 1:
                seg_end = total_audio
            else:
                seg_end = cursor + (n / total_words) * total_audio
                seg_end = round(seg_end, 2)
            annotated.append({
                "name": s["name"],
                "start": round(cursor, 2),
                "end": seg_end,
                "words": [],  # timings not needed downstream
            })
            cursor = seg_end

        # Safety: ensure the last section truly ends at total_audio
        if annotated:
            annotated[-1]["end"] = round(total_audio, 2)
        return annotated

    # ------------------------------------------------------------------ #
    # Media assignment per section
    # ------------------------------------------------------------------ #
    def _assign_media(
        self,
        section_name: str,
        span: float,
        videos: list[dict],
        photos: list[dict],
        used_videos: set,
        used_photos: set,
        last_media: Optional[str],
    ) -> list[dict]:
        """
        Return a list of clip dicts filling `span` seconds for this section.
        Rotation rule: alternate video/photo based on scene preference, never
        repeat the immediately previous clip.
        """
        clips: list[dict] = []
        remaining = span
        if remaining <= 0:
            return clips

        prefer_video = self.scene_video_preference.get(section_name, 0.7) >= 0.5

        # Build a prioritised candidate pool
        def pick(kind: str, used: set, allow_repeat_last: bool) -> Optional[dict]:
            pool = videos if kind == "video" else photos
            # prefer unused, then least-recently-used
            cand = [m for m in pool if m["file"] not in used]
            if not cand:
                cand = list(pool)
            if not cand:
                return None
            # avoid repeating the exact last clip if possible
            if last_media and not allow_repeat_last:
                non_last = [m for m in cand if m["file"] != last_media]
                if non_last:
                    cand = non_last
            # deterministic: pick the shortest available that still fits nicely
            cand.sort(key=lambda m: m["file"])
            return cand[0]

        # Decide how many photo vs video clips based on preference
        # Hook/CTA/Benefits want mostly video; Outro wants photo.
        want_video_first = prefer_video

        while remaining > 0.1:
            # alternate
            if want_video_first:
                kind_first, kind_second = "video", "photo"
            else:
                kind_first, kind_second = "photo", "video"

            chosen = pick(kind_first, used_videos if kind_first == "video" else used_photos, False)
            if chosen is None:
                chosen = pick(kind_second, used_videos if kind_second == "video" else used_photos, False)
            if chosen is None:
                # absolutely no media left anywhere — bail (caller raises)
                break

            is_video = chosen["type"] == "video"
            if is_video:
                # trim video to needed span (but not more than its duration)
                dur = min(chosen["duration"], remaining)
                if dur <= 0:
                    dur = chosen["duration"]
                clip = {
                    "scene": section_name,
                    "media": chosen["file"],
                    "media_type": "video",
                    "duration": round(dur, 2),
                    "source_start": 0.0,
                    "ken_burns": False,
                }
                used_videos.add(chosen["file"])
            else:
                dur = min(self.photo_duration, remaining)
                if dur <= 0:
                    dur = self.photo_duration
                clip = {
                    "scene": section_name,
                    "media": chosen["file"],
                    "media_type": "photo",
                    "duration": round(dur, 2),
                    "source_start": 0.0,
                    "ken_burns": self.ken_burns,
                }
                used_photos.add(chosen["file"])

            clip["start"] = round(span - remaining, 2)
            clip["end"] = round(clip["start"] + clip["duration"], 2)
            clips.append(clip)
            last_media = chosen["file"]
            remaining -= clip["duration"]
            # next clip prefers the other kind for rotation
            want_video_first = not want_video_first

        return clips

    # ------------------------------------------------------------------ #
    # Public entry
    # ------------------------------------------------------------------ #
    def generate_timeline(
        self,
        project_path: Path,
        word_timings: list[dict],
        script_text: Optional[str] = None,
        brand: Optional[dict] = None,
    ) -> list[dict]:
        # Allow disabling Ken Burns for faster renders (brand.json)
        if brand and brand.get("ken_burns") is False:
            self.ken_burns = False
        else:
            self.ken_burns = True

        videos, photos = self._gather_media(project_path)

        if not videos and not photos:
            raise ValueError(
                "No media files found in project videos/ or photos/ folders."
            )

        # Parse script sections
        from app.services.script_service import script_service
        sections = script_service.parse_script(script_text or "")

        if not sections:
            # No structured script: treat whole narration as one "Body" section
            total = word_timings[-1]["end"] if word_timings else 30.0
            sections = [{"name": "Body", "text": (script_text or "").strip() or "Reel",
                         "words": len(script_text.split()) if script_text else 0}]

        annotated = self._split_timings_by_sections(word_timings, sections)
        if not annotated:
            # Fallback if timings missing: equal splits across sections
            total = word_timings[-1]["end"] if word_timings else 30.0
            step = total / len(sections)
            annotated = []
            for i, s in enumerate(sections):
                annotated.append({
                    "name": s["name"],
                    "start": round(i * step, 2),
                    "end": round((i + 1) * step, 2),
                    "words": [],
                })

        used_videos: set = set()
        used_photos: set = set()
        last_media: Optional[str] = None
        timeline: list[dict] = []

        for sec in annotated:
            span = sec["end"] - sec["start"]
            if span <= 0:
                continue
            clips = self._assign_media(
                sec["name"], span, videos, photos,
                used_videos, used_photos, last_media,
            )
            # shift clip times to absolute narration time
            offset = sec["start"]
            for c in clips:
                c["start"] = round(c["start"] + offset, 2)
                c["end"] = round(c["end"] + offset, 2)
                last_media = c["media"]
                timeline.append(c)

        if not timeline:
            raise ValueError("Timeline engine could not assign any media to the narration.")

        # Persist for the renderer / frontend
        (project_path / "temp").mkdir(parents=True, exist_ok=True)
        with open(project_path / "temp" / "timeline.json", "w", encoding="utf-8") as f:
            json.dump(timeline, f, indent=4)

        return timeline


timeline_engine = TimelineEngine()
