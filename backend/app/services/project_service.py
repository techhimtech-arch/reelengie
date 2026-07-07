import os
import json
from pathlib import Path
from datetime import datetime

from app.core.config import settings

class ProjectService:
    def __init__(self):
        # Resolve the absolute path to the projects directory
        # The script is in backend/app/services, so root is 3 levels up
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.projects_dir = self.root_dir / settings.projects_dir
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, name: str, tree_name: str, day_number: int) -> dict:
        """
        Creates the folder structure for a new project and saves project.json.
        """
        project_id = name.strip().replace(" ", "_")
        project_path = self.projects_dir / project_id
        
        if project_path.exists():
            raise ValueError(f"Project '{project_id}' already exists.")

        # Create necessary directories
        directories = ['voice', 'script', 'videos', 'photos', 'output', 'logs', 'temp']
        for d in directories:
            (project_path / d).mkdir(parents=True, exist_ok=True)

        # Create project.json
        project_data = {
            "id": project_id,
            "name": name,
            "tree_name": tree_name,
            "day_number": day_number,
            "created_at": datetime.utcnow().isoformat(),
            "status": "created"
        }
        
        with open(project_path / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=4)

        return project_data

    def get_projects(self) -> list[dict]:
        """
        Returns a list of all projects by reading project.json files.
        """
        projects = []
        for p in self.projects_dir.iterdir():
            if p.is_dir():
                project_json = p / "project.json"
                if project_json.exists():
                    with open(project_json, "r", encoding="utf-8") as f:
                        projects.append(json.load(f))
        
        # Sort by created_at descending
        projects.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return projects

project_service = ProjectService()
