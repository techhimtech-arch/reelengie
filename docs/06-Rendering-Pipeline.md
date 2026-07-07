# Rendering Pipeline

Project: Reel Engine
Version: 0.1 MVP

---

# Objective

Convert a project folder into a finished vertical MP4 reel.

Rendering must be deterministic.

Same input should always generate the same output.

---

# Rendering Pipeline

Project

↓

Read Configuration

↓

Read Timeline

↓

Load Voice

↓

Load Videos

↓

Load Photos

↓

Generate Captions

↓

Prepare Clips

↓

Build Video Track

↓

Build Audio Track

↓

Overlay Branding

↓

Append Outro

↓

Export MP4

---

# Stage 1

Read Project

Read

project.json

timeline.json

script.txt

voice.mp3

brand.json

---

# Stage 2

Prepare Media

For every media

Read

Width

Height

Duration

FPS

Codec

Rotation

Orientation

Create metadata cache.

---

# Stage 3

Clip Preparation

Videos

Trim according to timeline.

Crop to 9:16.

Scale to 1080×1920.

Photos

Resize.

Apply Ken Burns.

Use timeline duration.

---

# Stage 4

Timeline Assembly

Append clips.

No gaps.

No overlap.

Maintain scene order.

---

# Stage 5

Caption Generation

Input

Voice timing

Output

captions.ass

Rules

Word highlighting

Bottom safe area

Never overlap logo

Use Himsols caption style

---

# Stage 6

Branding

Overlay logo

Bottom-right

Opacity configurable

Optional intro

Optional outro

---

# Stage 7

Audio

Primary Track

Narration

Secondary Track

Background Music

Rules

Narration = 100%

Music = 15–20%

Fade in = 1 sec

Fade out = 2 sec

Loop music if shorter than narration.

---

# Stage 8

Transitions

Default

Hard Cut

Optional

Fade

Cross Dissolve

No flashy transitions.

---

# Stage 9

Export

Resolution

1080 × 1920

FPS

30

Video Codec

H264

Audio Codec

AAC

Container

MP4

---

# Stage 10

Cleanup

Delete temporary files.

Keep only

timeline.json

project.json

output.mp4

render.log

---

# Folder Structure

projects/

project-name/

voice/

videos/

photos/

brand/

output/

logs/

temp/

---

# FFmpeg Responsibilities

Trim clips

Crop

Scale

Merge

Overlay logo

Burn captions

Mix audio

Append outro

Export

---

# Renderer Rules

Never stretch media.

Never distort aspect ratio.

Prefer crop over resize.

Keep visual quality high.

Avoid unnecessary re-encoding.

---

# Failure Recovery

If one media file is corrupt

Skip it.

Use next available media.

If logo missing

Continue rendering.

If background music missing

Render narration only.

If photo missing

Continue.

Rendering should fail only if

Voice missing

OR

No usable media exists.

---

# Render Progress

Frontend should receive

Preparing Media

10%

Generating Timeline

25%

Preparing Captions

40%

Rendering Video

70%

Final Encoding

90%

Completed

100%

---

# Logs

Every render generates

render.log

Include

Start Time

End Time

FFmpeg Commands

Errors

Warnings

Duration

Output Size

---

# Performance Goal

45–50 second reel

Target render time

Under 2 minutes

Modern laptop

---

# Future Rendering Features

GPU Encoding

Hardware Acceleration

4K Export

60 FPS

Batch Rendering

Multiple Export Presets

Cloud Rendering
