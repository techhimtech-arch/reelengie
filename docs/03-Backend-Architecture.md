# Backend Architecture

Project: Reel Engine
Version: MVP 0.1

---

# Philosophy

The backend is NOT a web application.

The backend is a rendering engine.

Its only responsibility is:

Receive project

↓

Process project

↓

Generate Reel

↓

Return MP4

Nothing else.

No database.

No users.

No authentication.

No cloud.

Everything runs locally.

---

# Backend Stack

Python 3.12+

FastAPI

FFmpeg

Whisper

MoviePy (only where FFmpeg becomes difficult)

OpenCV (optional)

Pydantic

Uvicorn

---

# Folder Structure

backend/

    app/

        api/

        services/

        models/

        utils/

        core/

        workers/

        templates/

        config/

        main.py

---

# Services

The backend is divided into small services.

Every service performs exactly one responsibility.

Never mix responsibilities.

---

# Upload Service

Purpose

Receive uploaded assets.

Responsibilities

Validate files

Create project folder

Save uploaded assets

Generate project.json

Output

Project Directory

---

# Voice Service

Purpose

Process narration.

Responsibilities

Load voice

Normalize audio

Generate speech timestamps

Generate subtitle timing

Return structured timing data

Output Example

[
  {
    "text":"Did you know",
    "start":0.0,
    "end":1.8
  }
]

---

# Script Service

Purpose

Read script.

Responsibilities

Split script into sections

Validate structure

Generate scene objects

Output

Scenes

Hook

Intro

Plantation

Benefits

CTA

Outro

---

# Timeline Engine

Purpose

Create timeline.

Input

Script

Voice timing

Available media

Output

Timeline

Example

Scene 1

Video

0-3

Scene 2

Photo

3-5

Scene 3

Video

5-9

Scene 4

Video

9-14

Scene 5

Photo

14-17

---

Timeline Rules

Never leave empty space.

Mix videos and photos naturally.

Never repeat same clip immediately.

Prefer unused media.

Respect scene duration.

---

# Media Service

Purpose

Inspect uploaded media.

Responsibilities

Read duration

Read dimensions

Read orientation

Generate thumbnail

Extract metadata

Output Example

{
  "filename":"watering.mp4",
  "duration":18.3,
  "width":1920,
  "height":1080,
  "orientation":"landscape"
}

---

# Caption Service

Purpose

Generate subtitle files.

Responsibilities

Create ASS subtitles

Apply Himsols style

Highlight current word

Safe margins

Return subtitle file

Output

captions.ass

---

# Branding Service

Purpose

Apply branding.

Responsibilities

Logo

Intro

Outro

Background music

Watermark

Color theme

---

# Renderer Service

Most important module.

Purpose

Generate final reel.

Responsibilities

Trim clips

Crop clips

Resize clips

Merge clips

Apply captions

Overlay logo

Mix music

Append outro

Export MP4

Output

output.mp4

---

# Export Service

Purpose

Move rendered video.

Responsibilities

Store inside

exports/

Return file path

Generate export metadata

---

# Logging Service

Purpose

Keep render logs.

Responsibilities

Render start

Render finish

Errors

FFmpeg commands

Timing

Output

logs/render.log

---

# Error Service

Purpose

Standardize errors.

Possible Errors

Voice Missing

Script Missing

Media Missing

FFmpeg Missing

Microphone Denied

Render Failed

Export Failed

Subtitle Failed

---

# API Layer

The frontend communicates only with FastAPI.

The frontend never calls FFmpeg directly.

Flow

Frontend

↓

API

↓

Services

↓

Renderer

↓

Response

---

# Processing Order

Upload

↓

Validate

↓

Voice Processing

↓

Script Parsing

↓

Timeline Generation

↓

Media Analysis

↓

Caption Generation

↓

Brand Overlay

↓

Rendering

↓

Export

↓

Done

---

# Threading

Rendering must run in background.

Frontend should never freeze.

Render progress should be available.

Example

5%

12%

31%

48%

71%

92%

100%

---

# Temporary Files

Use

temp/

Automatically delete after render.

Never keep unnecessary files.

---

# Configuration

Every project has

project.json

Every brand has

brand.json

Every export has

export.json

No configuration should be hardcoded.

---

# Design Principles

Small Services

Single Responsibility

No Business Logic Inside API Routes

No Hardcoded Paths

No Hardcoded Branding

Everything Configurable

Everything Replaceable
