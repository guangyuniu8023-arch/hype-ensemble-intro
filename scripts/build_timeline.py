#!/usr/bin/env python3
"""Build an exact ensemble-intro timeline using integer-second timecodes."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


MIN_DURATION = 9
MAX_DURATION = 30
MIN_CHARACTERS = 1
MAX_CHARACTERS = 12


@dataclass
class Beat:
    name: str
    start: int
    end: int


@dataclass
class CharacterSegment:
    character: str
    start: int
    end: int
    duration: int
    beats: list[Beat]


def final_duration(total: int) -> int:
    """Reserve an integer 20% finale, clamped to two through four seconds."""
    return min(4, max(2, (total * 2 + 5) // 10))


def minimum_duration_for_characters(characters: int) -> int:
    """Return the shortest supported duration with one full second per character."""
    if not MIN_CHARACTERS <= characters <= MAX_CHARACTERS:
        raise ValueError(
            f"characters must be between {MIN_CHARACTERS} and {MAX_CHARACTERS}"
        )
    for duration in range(MIN_DURATION, MAX_DURATION + 1):
        if duration - final_duration(duration) >= characters:
            return duration
    raise ValueError("no supported duration can accommodate this character count")


def distribute_seconds(total: int, buckets: int) -> list[int]:
    """Distribute whole seconds evenly, giving earlier buckets the remainder."""
    base, remainder = divmod(total, buckets)
    return [base + (1 if index < remainder else 0) for index in range(buckets)]


def split_three_beats(duration: int) -> list[int]:
    """Split a segment into entrance, skill, and confirmation in whole seconds."""
    if duration < 3:
        raise ValueError("three-beat segments require at least 3 seconds")

    weights = (28, 44, 28)
    lengths = [1, 1, 1]
    extra = duration - 3
    raw = [extra * weight / 100 for weight in weights]
    floors = [int(value) for value in raw]
    lengths = [length + floor for length, floor in zip(lengths, floors)]
    remainder = extra - sum(floors)
    order = sorted(
        range(3),
        key=lambda index: (raw[index] - floors[index], weights[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        lengths[index] += 1
    return lengths


def build_character_beats(start: int, end: int) -> list[Beat]:
    """Use compressed beat names when a character has fewer than 3 seconds."""
    duration = end - start
    if duration == 1:
        return [Beat("reveal_accelerate_skill_hit_confirm", start, end)]
    if duration == 2:
        return [
            Beat("entrance_and_accelerate", start, start + 1),
            Beat("signature_skill_hit_and_hero_confirm", start + 1, end),
        ]

    entrance, skill, confirm = split_three_beats(duration)
    entrance_end = start + entrance
    skill_end = entrance_end + skill
    return [
        Beat("entrance_and_accelerate", start, entrance_end),
        Beat("signature_skill_hit", entrance_end, skill_end),
        Beat("hero_confirm", skill_end, skill_end + confirm),
    ]


def build_group_beats(start: int, end: int) -> list[Beat]:
    """Build the complete team-formation climax without an automatic text-title beat."""
    duration = end - start
    if duration == 2:
        return [
            Beat("team_formation_reveal_landing_and_impact", start, start + 1),
            Beat("formation_lock_micro_motion_and_sound_tail", start + 1, end),
        ]
    if duration == 3:
        return [
            Beat("team_formation_reveal_and_full_band_impact", start, start + 1),
            Beat("character_landing_weapon_reset_and_formation_lock", start + 1, start + 2),
            Beat("heroic_group_micro_motion_and_sound_tail", start + 2, end),
        ]
    return [
        Beat("team_formation_reveal_and_full_band_impact", start, start + 1),
        Beat("character_landing_and_formation_build", start + 1, start + 2),
        Beat("formation_lock_with_staggered_micro_motion", start + 2, start + 3),
        Beat("heroic_group_hold_and_sound_tail", start + 3, end),
    ]


def build_timeline(duration: int, characters: int) -> dict:
    if not MIN_DURATION <= duration <= MAX_DURATION:
        raise ValueError(
            f"duration must be an integer between {MIN_DURATION} and {MAX_DURATION} seconds"
        )
    minimum_duration = minimum_duration_for_characters(characters)
    if duration < minimum_duration:
        raise ValueError(
            "integer-second timecodes require at least 1 second per character; "
            f"use a duration of at least {minimum_duration} seconds"
        )

    group_length = final_duration(duration)
    solo_length = duration - group_length
    segment_lengths = distribute_seconds(solo_length, characters)
    segments: list[CharacterSegment] = []
    cursor = 0

    for index, segment_length in enumerate(segment_lengths):
        start = cursor
        end = start + segment_length
        segments.append(
            CharacterSegment(
                character=f"C{index + 1}",
                start=start,
                end=end,
                duration=segment_length,
                beats=build_character_beats(start, end),
            )
        )
        cursor = end

    group_start = solo_length

    return {
        "duration": duration,
        "character_count": characters,
        "minimum_recommended_duration": minimum_duration,
        "solo_showcase": {
            "start": 0,
            "end": solo_length,
            "segment_lengths": segment_lengths,
            "segments": [
                {
                    **{k: v for k, v in asdict(segment).items() if k != "beats"},
                    "beats": [asdict(beat) for beat in segment.beats],
                }
                for segment in segments
            ],
        },
        "group_finale": {
            "start": group_start,
            "end": duration,
            "beats": [asdict(beat) for beat in build_group_beats(group_start, duration)],
        },
        "warning": (
            "Compressed solo beats: express anticipation and impact by ordered phases, "
            "or convert them to integer frames only when frame rate is explicit."
            if min(segment_lengths) < 2
            else None
        ),
    }


def recommendation(characters: int) -> dict:
    duration = minimum_duration_for_characters(characters)
    return {
        "character_count": characters,
        "minimum_recommended_duration": duration,
        "unit": "seconds",
        "note": "Recommendation only; do not override an explicit upstream duration.",
    }


def to_markdown(timeline: dict) -> str:
    lines = [
        f"Duration: {timeline['duration']}s",
        f"Characters: {timeline['character_count']}",
        f"Minimum recommended duration: {timeline['minimum_recommended_duration']}s",
        "",
        "| Segment | Start | End | Beat |",
        "| --- | ---: | ---: | --- |",
    ]
    for segment in timeline["solo_showcase"]["segments"]:
        beats = " → ".join(
            f"{beat['name']} {beat['start']}–{beat['end']}s"
            for beat in segment["beats"]
        )
        lines.append(
            f"| {segment['character']} | {segment['start']}s | "
            f"{segment['end']}s | {beats} |"
        )
    finale = timeline["group_finale"]
    for beat in finale["beats"]:
        lines.append(
            f"| Group | {beat['start']}s | {beat['end']}s | {beat['name']} |"
        )
    if timeline["warning"]:
        lines.extend(["", f"Warning: {timeline['warning']}"])
    return "\n".join(lines)


def recommendation_to_markdown(data: dict) -> str:
    return "\n".join(
        [
            f"Characters: {data['character_count']}",
            f"Suggested minimum duration: {data['minimum_recommended_duration']}s",
            "Status: recommendation only",
            f"Note: {data['note']}",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int)
    parser.add_argument("--characters", type=int, required=True)
    parser.add_argument("--minimum-only", action="store_true")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    try:
        if args.minimum_only:
            data = recommendation(args.characters)
            if args.format == "markdown":
                print(recommendation_to_markdown(data))
            else:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            return
        if args.duration is None:
            parser.error("--duration is required unless --minimum-only is used")
        timeline = build_timeline(args.duration, args.characters)
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "markdown":
        print(to_markdown(timeline))
    else:
        print(json.dumps(timeline, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
