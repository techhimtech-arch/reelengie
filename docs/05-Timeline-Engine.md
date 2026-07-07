# Timeline Engine

Version 0.1

---

# Purpose

Timeline Engine is responsible for converting

Script

+

Voice

+

Uploaded Media

into

A Render Timeline

It does NOT render video.

It only creates a timeline.

Renderer follows the timeline.

---

# Inputs

Script

Voice Timing

Uploaded Videos

Uploaded Photos

Brand Configuration

---

# Output

timeline.json

Example

[
    {
        "scene":"Hook",
        "media":"video3.mp4",
        "start":0,
        "end":3
    }
]

---

# Timeline Philosophy

Timeline should look natural.

Never repetitive.

Never random.

Never leave blank frames.

Every second should contain media.

---

# Reel Sections

Scene 1

Hook

---

Scene 2

Introduction

---

Scene 3

Plantation

---

Scene 4

Benefits

---

Scene 5

CTA

---

Scene 6

Outro

---

# Voice Alignment

Voice controls scene duration.

Never force scene duration.

Example

Hook

Voice Length

2.8 sec

Timeline

2.8 sec

NOT

3 sec fixed.

---

# Media Selection

Timeline Engine chooses media.

Priority

Relevant Media

↓

Unused Media

↓

Least Recently Used

↓

Random

---

# Media Types

Video

Photo

Both are equal.

Photos are not fallback.

Photos can appear anywhere.

---

# Clip Length

If video is longer

Trim.

If shorter

Move to next media.

Never freeze last frame.

---

# Photo Duration

Default

2.5 seconds

Configurable.

Ken Burns effect enabled.

---

# Video Duration

Use only required duration.

Never play full video unless needed.

---

# Scene Transition

Simple Cut

Preferred.

Optional

Fade

Cross Dissolve

Never use flashy transitions.

---

# Media Rotation

Bad

Video

Video

Video

Video

Good

Video

Photo

Video

Video

Photo

Video

---

# Duplicate Prevention

Never use same clip twice consecutively.

Try maximum diversity.

---

# Media Scoring

Every uploaded media receives score.

Example

Landscape

70

Portrait

100

Very Short

40

Too Long

80

High Resolution

100

Low Resolution

50

Timeline always picks highest score.

---

# Orientation Rules

Portrait

Preferred

Landscape

Auto Crop

Square

Center Crop

---

# Crop Rules

Never stretch.

Always crop.

Always keep center visible.

---

# Zoom Rules

Photos

Ken Burns

Videos

No zoom unless configured.

---

# Pacing

Hook

Fast

Plantation

Medium

Benefits

Slow

CTA

Medium

Outro

Slow

---

# Scene Objectives

Hook

Grab attention.

---

Introduction

Explain challenge.

---

Plantation

Show planting.

---

Benefits

Show plant.

Leaves.

Closeups.

Watering.

---

CTA

Final beauty shot.

---

Outro

Brand.

Logo.

Website.

---

# Timeline JSON

Example

[
  {
    "scene":"Hook",
    "start":0,
    "end":2.8,
    "media":"drone.mp4"
  },
  {
    "scene":"Intro",
    "start":2.8,
    "end":8.2,
    "media":"photo3.jpg"
  }
]

---

# Validation

Timeline must

Cover 100% narration.

Never overlap scenes.

Never create negative duration.

Never create empty timeline.

---

# Timeline Regeneration

User may regenerate.

Timeline should change media order.

Voice timing remains same.

---

# Future

AI Clip Recommendation

Computer Vision

Automatic Object Detection

Scene Detection

Emotion Detection

Smart Camera Motion
