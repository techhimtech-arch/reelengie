# Software Requirements Document (SRD)

# Project

Reel Engine

Version

0.1 MVP

---

# 1. Objective

Build a local-first application that automatically creates professional vertical reels from user supplied assets.

The application must edit uploaded media only.

No AI generated videos.

No cloud rendering.

No login.

No database.

Everything should run locally.

---

# 2. Target User

Primary User

Content Creator

Himsols Team

Future

Small Businesses

NGOs

Agencies

Marketing Teams

---

# 3. User Journey

User opens application.

↓

Create New Project

↓

Enter Project Name

↓

Enter Tree Name

↓

Enter Day Number

↓

Paste Script

↓

Record Voice
OR
Upload Voice

↓

Upload Videos

↓

Upload Photos

↓

Generate Reel

↓

Preview

↓

Export

Done.

---

# 4. Functional Requirements

## FR-001

User can create unlimited projects.

---

## FR-002

Each project is stored as a folder.

Example

projects/

Day01-Bamboo/

---

## FR-003

User can record voice directly inside application.

Required

Start Recording

Pause

Resume

Stop

Play Recording

Delete Recording

Re-record

---

## FR-004

User can upload voice.

Supported

MP3

WAV

M4A

---

## FR-005

User can paste script.

No JSON editing required.

---

## FR-006

User can upload unlimited videos.

Supported

MP4

MOV

---

## FR-007

User can upload unlimited photos.

Supported

JPG

PNG

WEBP

---

## FR-008

Generate Reel button.

Single click.

---

## FR-009

System automatically creates timeline.

---

## FR-010

System automatically synchronizes captions with narration.

---

## FR-011

System automatically inserts logo.

---

## FR-012

System automatically mixes background music.

---

## FR-013

System exports MP4.

---

# 5. Media Rules

Videos and photos should both be used.

Photos are NOT fallback media.

Example

Video

↓

Photo

↓

Video

↓

Video

↓

Photo

↓

Video

Timeline should feel natural.

---

No blank screen allowed.

---

No stretched media.

---

Crop using center crop.

---

Portrait media preferred.

Landscape media should be automatically cropped.

---

# 6. Voice Rules

User may

Record Voice

OR

Upload Voice

Only one narration track per project.

Background music is separate.

---

# 7. Script Rules

Script should be divided into sections.

Hook

Introduction

Plantation

Benefits

CTA

Outro

Each section should generate one scene.

---

# 8. Timeline Rules

Scene 1

Hook

0-3 sec

---

Scene 2

Introduction

3-8 sec

---

Scene 3

Plantation

8-22 sec

---

Scene 4

Benefits

22-38 sec

---

Scene 5

CTA

38-45 sec

---

Scene 6

Outro

45-50 sec

Durations may change slightly depending on narration.

---

# 9. Caption Rules

Generate captions from narration.

Word level highlighting.

Bottom safe area.

Never overlap logo.

Use Himsols theme.

---

# 10. Logo Rules

Bottom Right

Opacity configurable

Safe Margin

Visible during entire reel except intro animation if configured.

---

# 11. Background Music

Optional

If uploaded

Automatically reduce volume during narration.

Fade In

Fade Out

Loop if required.

---

# 12. Intro

Optional

Maximum

3 seconds

Skip if user disables.

---

# 13. Outro

Optional

Maximum

5 seconds

Can include

Logo

Website

Follow CTA

---

# 14. Preview

After rendering

User should preview reel.

Buttons

Play

Pause

Restart

Export

Regenerate

---

# 15. Export

MP4

1080 x 1920

30 FPS

H264

AAC Audio

High Quality

---

# 16. Non Functional Requirements

Local Processing

Fast Rendering

No Login

No Database

Offline Friendly

Reusable Components

Modular Backend

Production Ready Code

---

# 17. Error Handling

If no voice

Show error.

---

If no media

Show error.

---

If render fails

Keep logs.

Allow retry.

---

If FFmpeg missing

Show installation guide.

---

If microphone permission denied

Allow upload instead.

---

# 18. Project Folder

projects/

ProjectName/

voice/

script/

videos/

photos/

output/

logs/

project.json

---

# 19. Acceptance Criteria

Application is considered complete if user can

Create Project

↓

Paste Script

↓

Record Voice
OR
Upload Voice

↓

Upload Videos

↓

Upload Photos

↓

Generate Reel

↓

Preview

↓

Export

Without using any external editor.

---

# 20. Future Features

Timeline Editing

Replace Clip

Trim Clip

Batch Export

Multiple Brand Templates

AI Clip Recommendation

AI Voice Cleanup

Automatic Thumbnail

Auto Hashtags

YouTube Upload

Instagram Upload

Cloud Rendering