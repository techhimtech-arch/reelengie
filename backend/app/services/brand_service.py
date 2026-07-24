"""
Branding Service
================
Loads the project's brand configuration from `brand/brand.json` and exposes
helpers so the timeline engine and renderer can apply consistent branding:

  * Logo (bottom-right, configurable opacity, safe margin)
  * Background music (optional, ducked under narration, fade in/out)
  * Intro (optional, max 3s)
  * Outro (optional, max 5s, can include logo + website + follow CTA)

All rules follow docs/06-Rendering-Pipeline.md (Branding + Audio stages).

If `brand/brand.json` or any asset is missing, the service degrades gracefully:
the renderer simply skips that branding element instead of failing.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


class BrandService:
    # Sensible defaults so a project works even without a brand.json
    DEFAULTS = {
        "logo": None,                 # filename inside brand/
        "logo_opacity": 0.9,          # 0..1
        "logo_margin": 0.04,          # fraction of width as safe margin
        "logo_scale": 0.22,           # fraction of width the logo occupies
        "music": None,                # filename inside brand/
        "music_volume": 0.18,         # 0..1 (ducked under narration)
        "music_fade_in": 1.0,
        "music_fade_out": 2.0,
        "intro": None,                # filename inside brand/
        "intro_max_duration": 3.0,
        "outro": None,                # filename inside brand/
        "outro_max_duration": 5.0,
        "ken_burns": True,            # slow zoom on photos; false = faster render
        "caption_style": "himsols",
        "primary_color": "&H00FFFFFF",   # white
        "highlight_color": "&H0000FFFF", # yellow
    }

    def __init__(self):
        pass

    def load(self, project_path: Path) -> dict:
        """Load brand config for a project. Returns a merged dict with defaults."""
        brand_dir = project_path / "brand"
        config_path = brand_dir / "brand.json"
        config: dict = {}
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f) or {}
            except Exception:
                config = {}

        merged = dict(self.DEFAULTS)
        merged.update(config)

        # Resolve asset paths if present
        for key in ("logo", "music", "intro", "outro"):
            fname = merged.get(key)
            if fname:
                p = brand_dir / fname
                merged[key] = str(p) if p.exists() else None
            else:
                merged[key] = None

        return merged


brand_service = BrandService()
