# Reel Engine

Local-first automatic reel rendering engine. Edits uploaded media into vertical social reels — no AI video generation, no cloud, no database.

## Documentation

All specifications live in [`/docs`](./docs):

| Doc | Description |
|---|---|
| [00-Project-Vision.md](./docs/00-Project-Vision.md) | Product vision and principles |
| [01-SRD.md](./docs/01-SRD.md) | Software requirements (MVP 0.1) |
| [02-System-Architecture.md](./docs/02-System-Architecture.md) | System architecture |
| [03-Backend-Architecture.md](./docs/03-Backend-Architecture.md) | Backend services |
| [04-Frontend-Architecture.md](./docs/04-Frontend-Architecture.md) | Wizard workflow |
| [05-Timeline-Engine.md](./docs/05-Timeline-Engine.md) | Timeline generation rules |
| [06-Rendering-Pipeline.md](./docs/06-Rendering-Pipeline.md) | FFmpeg rendering pipeline |

## Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, TailwindCSS, Electron |
| Backend | Python 3.12+, FastAPI, Uvicorn, Pydantic |
| Rendering | FFmpeg, Whisper |

## Prerequisites

- Python 3.12+
- Node.js 20+
- FFmpeg (with `ffprobe`) on PATH

## Setup

```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd ..\frontend
npm install
```

Copy `.env.example` to `.env` and adjust if needed.

## Development

```powershell
# Terminal 1 — backend
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8765

# Terminal 2 — frontend
cd frontend
npm run dev
```

Or use the root script:

```powershell
.\scripts\dev.ps1
```

## Tests

```powershell
cd backend
pytest
```

## Project Structure

```
reelengie/
  backend/       Python FastAPI rendering engine
  frontend/      React + Vite UI
  electron/      Desktop shell
  docs/          Source of truth specifications
  projects/      Local project folders (gitignored)
  scripts/       Dev utilities
```
