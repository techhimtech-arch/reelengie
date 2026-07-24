from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.project_service import project_service

router = APIRouter()

class ProjectCreateRequest(BaseModel):
    name: str
    tree_name: str
    day_number: int

class ProjectResponse(BaseModel):
    id: str
    name: str
    tree_name: str
    day_number: int
    created_at: str
    status: str

@router.post("/", response_model=ProjectResponse)
def create_project(request: ProjectCreateRequest):
    try:
        project_data = project_service.create_project(
            name=request.name,
            tree_name=request.tree_name,
            day_number=request.day_number
        )
        return project_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/", response_model=List[ProjectResponse])
def get_projects():
    try:
        return project_service.get_projects()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

class TimelineClip(BaseModel):
    scene: str
    start: float
    end: float
    source_start: float = 0.0
    media: str
    media_type: str

class TimelineUpdateRequest(BaseModel):
    timeline: List[TimelineClip]

@router.post("/{project_id}/timeline")
def generate_timeline(project_id: str):
    try:
        from app.services.voice_service import voice_service
        from app.services.caption_service import caption_service
        from app.services.timeline_engine import timeline_engine
        from app.services.project_service import project_service
        import os
        import json

        project_path = project_service.projects_dir / project_id
        
        # 1. Find audio file
        voice_dir = project_path / 'voice'
        audio_files = os.listdir(voice_dir) if voice_dir.exists() else []
        if not audio_files:
            raise ValueError("No voice file found. Please upload a voice recording first.")
        audio_path = str(voice_dir / audio_files[0])

        # 1.5 Find script file
        script_dir = project_path / 'script'
        script_text = None
        if script_dir.exists():
            script_files = [f for f in os.listdir(script_dir) if f.endswith('.txt')]
            if script_files:
                try:
                    with open(script_dir / script_files[0], 'r', encoding='utf-8') as f:
                        script_text = f.read()
                except Exception:
                    pass

        # 2. Run Whisper for timings
        word_timings = voice_service.transcribe_voice(audio_path, script_text=script_text)

        # 3. Generate Subtitles (needed for final render, generate early or save timings)
        subtitle_path = str(project_path / 'temp' / 'captions.ass')
        caption_service.generate_ass_file(word_timings, subtitle_path)

        # 4. Generate Timeline (scene/section-aware, brand-aware)
        from app.services.brand_service import brand_service
        brand = brand_service.load(project_path)
        timeline = timeline_engine.generate_timeline(
            project_path, word_timings, script_text=script_text, brand=brand
        )

        return {"status": "success", "timeline": timeline, "brand": brand}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/render")
def render_project(project_id: str, request: TimelineUpdateRequest = None):
    try:
        from app.services.render_service import render_service
        from app.services.project_service import project_service
        import os
        import json

        project_path = project_service.projects_dir / project_id
        
        # 1. Find audio file
        voice_dir = project_path / 'voice'
        audio_files = os.listdir(voice_dir) if voice_dir.exists() else []
        if not audio_files:
            raise ValueError("No voice file found. Please upload a voice recording first.")
        audio_path = str(voice_dir / audio_files[0])

        subtitle_path = str(project_path / 'temp' / 'captions.ass')
        
        if request and request.timeline:
            timeline = [clip.dict() for clip in request.timeline]
            with open(project_path / 'temp' / 'timeline.json', 'w', encoding='utf-8') as f:
                json.dump(timeline, f, indent=4)
        else:
            with open(project_path / 'temp' / 'timeline.json', 'r', encoding='utf-8') as f:
                timeline = json.load(f)

        # Load brand config (logo / music / intro / outro)
        from app.services.brand_service import brand_service
        brand = brand_service.load(project_path)

        # 5. Render Video (now brand-aware: logo overlay, music mix, ken burns)
        output_mp4 = render_service.render(
            project_path, timeline, audio_path, subtitle_path, brand=brand
        )

        return {"status": "success", "output": output_mp4}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

