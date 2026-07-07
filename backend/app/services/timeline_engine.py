import json
import random
from pathlib import Path

class TimelineEngine:
    def __init__(self):
        # Default durations if voice is missing or sections are misaligned
        self.default_scene_durations = {
            "Hook": 3.0,
            "Intro": 5.0,
            "Plantation": 14.0,
            "Benefits": 16.0,
            "CTA": 7.0,
            "Outro": 5.0
        }

    def generate_timeline(self, project_path: Path, voice_timings: list[dict]) -> list[dict]:
        """
        Generates a timeline mapping media to specific time segments.
        This is a simplified timeline generator that mixes available photos and videos.
        """
        # 1. Calculate total duration from voice timings
        total_duration = voice_timings[-1]['end'] if voice_timings else sum(self.default_scene_durations.values())
        
        # 2. Gather available media
        import subprocess
        
        videos_dir = project_path / 'videos'
        photos_dir = project_path / 'photos'
        
        media_items = []
        
        if videos_dir.exists():
            for v in videos_dir.iterdir():
                if v.is_file():
                    try:
                        dur_str = subprocess.check_output([
                            "ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of",
                            "default=noprint_wrappers=1:nokey=1", str(v)
                        ]).decode().strip()
                        dur = float(dur_str)
                    except Exception:
                        dur = 5.0
                    media_items.append({"file": v.name, "type": "video", "duration": dur})
                    
        if photos_dir.exists():
            for p in photos_dir.iterdir():
                if p.is_file():
                    media_items.append({"file": p.name, "type": "photo", "duration": 0.0})
                    
        if not media_items:
            raise ValueError("No media files found in projects folder.")
            
        # Shuffle media for variety
        random.shuffle(media_items)
        
        # 3. Calculate durations to avoid repetition
        videos_total_dur = sum(m["duration"] for m in media_items if m["type"] == "video")
        photos_count = sum(1 for m in media_items if m["type"] == "photo")
        
        if photos_count > 0:
            remaining_time = total_duration - videos_total_dur
            if remaining_time < photos_count * 2.0:
                photo_dur = 2.0
            else:
                photo_dur = remaining_time / photos_count
                
            for m in media_items:
                if m["type"] == "photo":
                    m["duration"] = photo_dur
        
        # 4. Create Timeline
        timeline = []
        current_time = 0.0
        
        for m in media_items:
            if current_time >= total_duration:
                break
                
            clip_dur = m["duration"]
            if current_time + clip_dur > total_duration:
                clip_dur = total_duration - current_time
                
            clip_end = current_time + clip_dur
            
            # Simple scene naming based on time
            scene_name = "Scene"
            if current_time < 3:
                scene_name = "Hook"
            elif current_time > total_duration - 5:
                scene_name = "Outro"
                
            timeline.append({
                "scene": scene_name,
                "start": round(current_time, 2),
                "end": round(clip_end, 2),
                "media": m["file"],
                "media_type": m["type"]
            })
            
            current_time = clip_end
            
        # Save timeline.json
        with open(project_path / 'temp' / 'timeline.json', 'w', encoding='utf-8') as f:
            json.dump(timeline, f, indent=4)
            
        return timeline

timeline_engine = TimelineEngine()
