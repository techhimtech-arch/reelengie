import os
import sys
from pathlib import Path

# Add FFmpeg to PATH dynamically
ffmpeg_path = r"C:\Users\hp\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

from app.api.routers.projects import render_project

try:
    print("Starting render process for project bael_tree...")
    result = render_project("bael_tree")
    print(f"Success! Output: {result}")
except Exception as e:
    import traceback
    traceback.print_exc()
