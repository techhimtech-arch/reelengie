# System Architecture

Project: Reel Engine

Version: 0.1 MVP

---

# Overview

Reel Engine is a local-first automatic reel generation application.

The application converts user supplied assets into a professional vertical social media reel.

The application never generates AI videos.

It only edits uploaded media.

The application is designed for internal use.

No authentication.

No database.

No cloud dependency.

---

# High Level Architecture

+--------------------------------------------------------+
|                   React + Electron                     |
|--------------------------------------------------------|
| Dashboard                                              |
| Project Wizard                                         |
| Voice Recorder                                         |
| Media Upload                                            |
| Preview Player                                         |
| Export Screen                                          |
+-----------------------------+--------------------------+
                              |
                              |
                              v
+--------------------------------------------------------+
|                  Python Backend                        |
|--------------------------------------------------------|
| Upload Service                                         |
| Project Service                                        |
| Voice Service                                          |
| Script Service                                         |
| Timeline Engine                                        |
| Media Service                                          |
| Caption Service                                        |
| Branding Service                                       |
| Render Service                                         |
| Export Service                                         |
+-----------------------------+--------------------------+
                              |
                              |
                              v
+--------------------------------------------------------+
|                 Rendering Engine                       |
|--------------------------------------------------------|
| FFmpeg                                                 |
| Whisper                                                |
| ASS Subtitle Generator                                 |
| Image Processing                                       |
| Audio Processing                                       |
+-----------------------------+--------------------------+
                              |
                              |
                              v
+--------------------------------------------------------+
|                    Project Folder                      |
|--------------------------------------------------------|
| Voice                                                  |
| Script                                                 |
| Videos                                                 |
| Photos                                                 |
| Timeline                                               |
| Output                                                 |
| Logs                                                   |
+--------------------------------------------------------+

---

# Application Layers

Layer 1

Frontend

Responsibilities

Create Project

Upload Assets

Record Voice

Preview

Export

No rendering logic.

---

Layer 2

Backend

Responsibilities

Receive project

Validate assets

Create timeline

Generate subtitles

Prepare render job

Start renderer

Return progress

---

Layer 3

Rendering Engine

Responsibilities

Trim clips

Resize clips

Crop media

Merge media

Mix audio

Burn subtitles

Overlay logo

Generate final MP4

---

Layer 4

Storage

Responsibilities

Store project

Store exports

Store temporary files

Store logs

No SQL database.

Everything stored inside folders.

---

# Request Flow

User

↓

Create Project

↓

Upload Assets

↓

Generate Reel

↓

Backend validates assets

↓

Voice Processing

↓

Script Processing

↓

Timeline Generation

↓

Caption Generation

↓

Rendering

↓

Preview

↓

Export

---

# Project Folder

projects/

project-name/

    project.json

    voice/

        narration.mp3

    script/

        script.txt

    videos/

    photos/

    output/

        reel.mp4

    logs/

        render.log

    temp/

---

# Internal Services

Project Service

Creates projects.

Loads projects.

Deletes projects.

---

Voice Service

Reads narration.

Normalizes audio.

Generates word timings.

Creates subtitle timing.

---

Script Service

Reads script.

Splits into scenes.

Validates required sections.

---

Timeline Engine

Builds render timeline.

Assigns media.

Creates timeline.json.

---

Media Service

Reads media metadata.

Creates thumbnails.

Determines orientation.

Calculates duration.

---

Caption Service

Generates captions.

Creates ASS subtitle file.

Synchronizes timing.

---

Brand Service

Applies

Logo

Intro

Outro

Music

Caption Style

---

Render Service

Reads timeline.

Builds FFmpeg command.

Executes rendering.

Tracks progress.

---

Export Service

Moves final video.

Stores metadata.

Returns file path.

---

# Communication Flow

Frontend

↓

Backend

↓

Timeline Engine

↓

Renderer

↓

Frontend receives progress

↓

Frontend receives output

---

# Processing Pipeline

Create Project

↓

Store Assets

↓

Validate

↓

Read Voice

↓

Generate Timings

↓

Read Script

↓

Create Scenes

↓

Analyze Media

↓

Build Timeline

↓

Generate Captions

↓

Prepare Render

↓

Render

↓

Export

↓

Complete

---

# Temporary Files

During rendering

temp/

contains

normalized_audio.wav

captions.ass

timeline.json

render_script.json

These files are deleted after successful render.

---

# Logging

Each render generates

render.log

Contains

Start Time

End Time

Render Duration

Errors

Warnings

FFmpeg Commands

Output Size

---

# Configuration Files

project.json

Contains

Project Name

Tree Name

Day Number

Location

Created Date

---

brand.json

Contains

Logo

Colors

Font

Music

Intro

Outro

Caption Theme

---

export.json

Contains

Resolution

FPS

Codec

Audio Settings

Export Quality

---

# Error Recovery

If one media file fails

Skip it

Continue rendering

If logo missing

Continue

If music missing

Continue

If intro missing

Continue

Rendering stops only when

Voice is missing

OR

No usable media exists

---

# Design Principles

Single Responsibility

Small Services

Modular Architecture

Reusable Components

No Business Logic in UI

No Hardcoded Paths

No Hardcoded Assets

Everything Configurable

Everything Replaceable

---

# Future Architecture

Timeline Editor

Clip Replacement

AI Clip Recommendation

Computer Vision

GPU Rendering

Cloud Rendering

Public SaaS

Plugin Support

Batch Rendering

Multiple Brand Profiles
