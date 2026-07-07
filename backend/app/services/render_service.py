import subprocess
import os
from pathlib import Path

class RenderService:
    def __init__(self):
        pass

    def build_ffmpeg_command(self, project_path: Path, timeline: list[dict], audio_path: str, subtitle_path: str) -> list[str]:
        """
        Builds the FFmpeg command based on the timeline.
        This is a basic FFmpeg construction that handles simple concatenation.
        """
        output_path = project_path / 'output' / 'output.mp4'
        
        # We construct a complex filter for FFmpeg
        inputs = []
        filter_complex = []
        
        # 1. Add Audio Input
        inputs.extend(['-i', audio_path])
        
        # 2. Add Media Inputs & Scale
        for idx, clip in enumerate(timeline):
            media_folder = 'videos' if clip['media_type'] == 'video' else 'photos'
            media_path = project_path / media_folder / clip['media']
            
            # Input file (idx + 1 because audio is 0)
            if clip['media_type'] == 'photo':
                inputs.extend(['-loop', '1', '-framerate', '30'])
            inputs.extend(['-t', str(clip['end'] - clip['start'])])
            inputs.extend(['-i', str(media_path)])
            
            input_idx = idx + 1
            # Scale to 1080x1920 (Crop and pad)
            filter_complex.append(
                f"[{input_idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v{idx}]"
            )
        
        # 3. Concat all videos
        concat_inputs = "".join([f"[v{i}]" for i in range(len(timeline))])
        filter_complex.append(f"{concat_inputs}concat=n={len(timeline)}:v=1:a=0[vconcat]")
        
        # 4. Burn subtitles
        subtitle_rel = os.path.relpath(subtitle_path).replace('\\', '/')
        filter_complex.append(f"[vconcat]ass='{subtitle_rel}'[vfinal]")
        
        # Compile final command
        cmd = [
            'ffmpeg', '-y',
            *inputs,
            '-filter_complex', ";".join(filter_complex),
            '-map', '[vfinal]',
            '-map', '0:a',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '24',
            '-c:a', 'aac',
            str(output_path)
        ]
        
        return cmd

    def render(self, project_path: Path, timeline: list[dict], audio_path: str, subtitle_path: str) -> str:
        cmd = self.build_ffmpeg_command(project_path, timeline, audio_path, subtitle_path)
        
        log_path = project_path / 'logs' / 'render.log'
        with open(log_path, 'w') as log_file:
            process = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True
            )
            process.wait()
            
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg render failed. Check logs at {log_path}")
            
        return str(project_path / 'output' / 'output.mp4')

render_service = RenderService()
