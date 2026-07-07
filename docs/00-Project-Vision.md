# Project Vision

# Project Name

Reel Engine

---

# Objective

Reel Engine is a local-first AI-assisted automatic video editing application.

The goal is NOT to generate AI videos.

The goal is to automatically edit videos provided by the user into professional Instagram Reels, YouTube Shorts and Facebook Reels.

The application should reduce reel creation time from 2–3 hours to less than 5 minutes.

---

# Target User

Initially:

Single User

Internal Tool

Later:

Small Teams

Eventually:

SaaS Product

---

# Primary Problem

Currently every reel requires:

- Writing script
- Recording voice
- Importing videos
- Importing photos
- Adding captions
- Adding logo
- Adding music
- Syncing everything manually
- Exporting

This process is repetitive.

Every reel follows almost the same structure.

Only the content changes.

---

# Proposed Solution

The user provides:

- Tree Name
- Day Number
- Voice
- Script
- Videos
- Photos

The application automatically:

- Creates timeline
- Synchronizes voice
- Places videos/photos
- Generates captions
- Adds logo
- Adds music
- Adds intro
- Adds outro
- Exports final MP4

---

# Product Philosophy

The application is NOT an editor.

It is an automatic rendering engine.

The user should spend time creating good content.

The software should do all repetitive editing.

---

# Core Principles

1.

No AI generated videos.

Only edit uploaded media.

---

2.

Everything should work offline.

Internet should not be required except optional AI features.

---

3.

No database required.

Projects are folders.

---

4.

No authentication.

No login.

No signup.

---

5.

No cloud dependency.

Everything should run locally.

---

6.

Deterministic output.

Same input should always generate the same output.

---

# Supported Input

Voice

- Record using microphone

OR

- Upload MP3/WAV

---

Script

Paste into editor.

No JSON editing required.

The application will convert it internally.

---

Media

Videos

Photos

---

Brand Assets

Logo

Background Music

Intro

Outro

---

# Supported Output

Instagram Reel

YouTube Shorts

Facebook Reel

TikTok

Resolution

1080x1920

FPS

30

Codec

H264

Audio

AAC

---

# Standard Reel Structure

0-3 sec

Hook

---

3-8 sec

Introduction

---

8-22 sec

Plantation

---

22-38 sec

Benefits

---

38-45 sec

Call To Action

---

45-50 sec

Outro

---

This structure remains fixed.

Only content changes.

---

# Editing Rules

Use videos whenever available.

Photos may appear anywhere.

Photos are NOT only fallback.

Timeline engine should intelligently mix photos and videos.

No blank frames.

No stretched media.

Always maintain aspect ratio.

---

# Caption Rules

Generate captions automatically.

Highlight current spoken word.

Keep captions inside safe area.

Use predefined Himsols caption style.

---

# Branding

Same logo

Same font

Same intro

Same outro

Same music

Same colors

Every reel should have consistent branding.

---

# Performance Goal

Generating a reel should take less than:

2 minutes

on a modern laptop.

---

# Future Scope

Timeline editor

Clip replacement

AI clip recommendation

Multiple themes

Multiple brands

Batch rendering

YouTube automation

Cloud rendering

Public SaaS

---

# Success Criteria

The project is successful if a user can:

Create Project

↓

Paste Script

↓

Record Voice OR Upload Voice

↓

Upload Videos

↓

Upload Photos

↓

Click Generate

↓

Preview

↓

Export MP4

Without opening CapCut.