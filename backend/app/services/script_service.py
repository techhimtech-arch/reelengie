"""
Script Service
==============
Reads the narration script (script/script.txt) and splits it into ordered
sections. Section headers use the bracket syntax, e.g.:

    [Hook]
    Did you know...?

    [Plantation]
    Today we planted...

Recognised section names (case-insensitive, see docs/01-SRD.md §7 and
docs/05-Timeline-Engine.md §Reel Sections):
    Hook, Introduction/Intro, Plantation, Benefits, CTA/Call To Action, Outro

If a script has NO section headers, the whole text is treated as a single
"Body" section (still rendered). If headers are present but a known section
is missing, it is simply absent from the timeline (voice-aligned gaps are
handled by the timeline engine).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


# Map aliases -> canonical scene name used by the timeline engine
_SECTION_ALIASES = {
    "hook": "Hook",
    "introduction": "Intro",
    "intro": "Intro",
    "plantation": "Plantation",
    "benefits": "Benefits",
    "cta": "CTA",
    "call to action": "CTA",
    "outro": "Outro",
    # Generic fallback name if a custom header is used
}
_HEADER_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$", re.IGNORECASE)


class ScriptService:
    def __init__(self):
        pass

    def parse_script(self, script_text: str) -> list[dict]:
        """
        Returns a list of section dicts:
            [{"name": "Hook", "text": "Did you know...", "words": 12}, ...]
        """
        if not script_text or not script_text.strip():
            return []

        lines = script_text.splitlines()
        sections: list[dict] = []
        current_name: Optional[str] = None
        current_lines: list[str] = []

        def flush():
            if current_name is None and not current_lines:
                return
            name = current_name if current_name else "Body"
            text = " ".join(l.strip() for l in current_lines if l.strip())
            if text:
                sections.append({
                    "name": name,
                    "text": text,
                    "words": len(text.split()),
                })

        for line in lines:
            m = _HEADER_RE.match(line)
            if m:
                # New section header
                flush()
                raw = m.group(1).strip()
                canon = _SECTION_ALIASES.get(raw.lower())
                current_name = canon if canon else raw  # preserve custom names
                current_lines = []
            else:
                current_lines.append(line)

        flush()

        # If everything landed in a single "Body" but the text clearly has
        # our known keywords, leave it — the timeline engine will still work.
        return sections


script_service = ScriptService()
