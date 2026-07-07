import shutil
from pathlib import Path
from fastapi import UploadFile

from app.core.config import settings

class UploadService:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.projects_dir = self.root_dir / settings.projects_dir

    def save_file(self, project_id: str, folder_type: str, file: UploadFile) -> str:
        """
        Saves an uploaded file to the specified project subfolder.
        """
        project_path = self.projects_dir / project_id
        if not project_path.exists():
            raise ValueError(f"Project '{project_id}' not found.")
            
        target_dir = project_path / folder_type
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            
        file_path = target_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return str(file_path)
        
    def save_script(self, project_id: str, script_content: str) -> str:
        """
        Saves the script text to script/script.txt
        """
        project_path = self.projects_dir / project_id
        if not project_path.exists():
            raise ValueError(f"Project '{project_id}' not found.")
            
        target_dir = project_path / 'script'
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            
        file_path = target_dir / "script.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script_content)
            
        return str(file_path)

upload_service = UploadService()
