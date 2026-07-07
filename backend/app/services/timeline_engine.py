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
        media_files = []
        videos_dir = project_path / 'videos'
        photos_dir = project_path / 'photos'
        
        if videos_dir.exists():
            media_files.extend([f.name for f in videos_dir.iterdir() if f.is_file()])
        if photos_dir.exists():
            media_files.extend([f.name for f in photos_dir.iterdir() if f.is_file()])
            
        if not media_files:
            raise ValueError("No media files found in projects folder.")
            
        # Shuffle media for variety
        random.shuffle(media_files)
        
        # 3. Create Timeline
        # We will create 3-4 second clips to fill the total duration
        timeline = []
        current_time = 0.0
        clip_duration = 3.5
        media_index = 0
        
        while current_time < total_duration:
            end_time = min(current_time + clip_duration, total_duration)
            media = media_files[media_index % len(media_files)]
            
            # Simple scene naming based on time
            scene_name = "Scene"
            if current_time < 3:
                scene_name = "Hook"
            elif current_time > total_duration - 5:
                scene_name = "Outro"
                
            timeline.append({
                "scene": scene_name,
                "start": round(current_time, 2),
                "end": round(end_time, 2),
                "media": media,
                "media_type": "video" if media.lower().endswith(('.mp4', '.mov')) else "photo"
            })
            
            current_time = end_time
            media_index += 1
            
        # Save timeline.json
        with open(project_path / 'temp' / 'timeline.json', 'w', encoding='utf-8') as f:
            json.dump(timeline, f, indent=4)
            
        return timeline

timeline_engine = TimelineEngine()
