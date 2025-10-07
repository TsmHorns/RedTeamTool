"""CivicBuildAssistant: generate non-professional temporary ramp guidance."""
from __future__ import annotations

import sys
from typing import Dict, List


REQUIRED_FIELDS = {
    "photo description": "photo description",
    "measured step height": "measured step height",
    "door swing": "door swing",
}

PLACEHOLDER_PREFIX = "<INSERT"


def _normalize(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip()


def parse_context(text: str) -> Dict[str, str]:
    context: Dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        context[key.strip().lower()] = value.strip()
    return context


def missing_required_fields(context: Dict[str, str]) -> List[str]:
    missing: List[str] = []
    for key, label in REQUIRED_FIELDS.items():
        value = _normalize(context.get(key))
        if not value or value.upper() == "UNKNOWN" or value.startswith(PLACEHOLDER_PREFIX):
            missing.append(label)
    return missing


def format_plan(context: Dict[str, str]) -> str:
    location = _normalize(context.get("location name")) or "the site"
    photo_description = _normalize(context.get("photo description"))
    height = _normalize(context.get("measured step height"))
    door_swing = _normalize(context.get("door swing"))
    budget_level = (_normalize(context.get("budget level")) or "unspecified").lower()
    volunteer_skill = (_normalize(context.get("volunteer skill level")) or "unspecified").lower()
    site_constraints = _normalize(context.get("any site constraints")) or "None noted"

    budget_notes = {
        "low": "Expect basic portable ramp panels or loaner equipment, plus anti-slip coverings.",
        "medium": "Allows sturdier modular sections, edge protectors, and temporary rails.",
        "high": "Could cover custom-fabricated modular systems and professional consultation fees.",
    }

    budget_comment = budget_notes.get(budget_level, "Budget level not specified; costs depend on materials and rental options available.")

    summary_sentence = (
        f"Provide a volunteer-assembled temporary ramp solution at {location} suited to a {volunteer_skill} volunteer team, with emphasis on gentle slope and non-slip surfaces; confirm measurements on-site because photos may hide conditions."
    )
    uncertainties = []
    if "unknown" in height.lower():
        uncertainties.append("exact step height")
    if "unknown" in door_swing.lower():
        uncertainties.append("door swing direction")
    if uncertainties:
        summary_sentence += " Key uncertainties: " + ", ".join(uncertainties) + "."

    materials_lines = [
        "Portable or modular ramp panels rated for temporary community use",
        "Surface traction aids such as anti-slip tape or outdoor matting",
        "Sturdy edging or visual markers to define ramp boundaries",
        "Temporary handrail kit or freestanding support posts (rental or modular)",
        "Basic fastening supplies like zip ties, straps, or clamps for temporary stabilization",
        "Tools: measuring tape, bubble level, broom, cordless drill/driver with assorted bits",
        "High-visibility cones or signage to alert approaching visitors",
    ]

    checklist_lines = [
        "Confirm permission from the Eastwood Community Center representative before any setup.",
        "Re-measure step height, landing depth, and surrounding clearances with two volunteers for accuracy.",
        "Inspect the existing surface for cracks, debris, or moisture; clean the area thoroughly.",
        "Dry-fit modular ramp pieces on level ground to understand orientation before moving to the doorway.",
        "Position ramp gently against the step, ensuring the transition plate sits flush without forcing it.",
        "Apply temporary traction aids and edge markers; verify they adhere securely without creating tripping hazards.",
        "Have multiple volunteers walk and roll test the ramp slowly while another spotter watches for shifting.",
        "Document the setup with photos and notes to share with a licensed contractor for review.",
    ]

    safety_notes = [
        "Always consult the local building department and a licensed contractor or accessibility specialist before installation, even for temporary use.",
        "Stop work if structural weaknesses, loose concrete, or drainage issues are observed; these require professional evaluation.",
        "Ensure volunteers wear gloves, closed-toe shoes, and high-visibility vests; use caution when lifting heavier panels.",
        "Do not leave the ramp unattended without railings or edge protection if the landing space is narrow.",
        "Verify liability coverage with the community center; temporary ramps can still pose risks if improperly supervised.",
    ]

    resources_lines = [
        "Local building department — confirm permit requirements for temporary accessibility structures.",
        "Municipal disability services office or advocacy group — request guidance on compliant access practices.",
        "Licensed contractors specializing in accessibility — schedule a consultation for design validation.",
        "Volunteer centers or tool libraries — inquire about loaner modular ramp systems or safety training.",
    ]

    budget_section = (
        "Low range: borrow or rent a portable ramp and minimal traction materials.\n"
        "Medium range: purchase modular ramp segments, temporary rail supports, and weather-resistant finishes.\n"
        "High range: invest in premium modular systems, professional assessments, and contingency supplies."
    )

    closing_guidance = (
        "Next steps: capture precise measurements (rise, run, landing depth), contact the building department about permits, and arrange a licensed contractor walkthrough before volunteers proceed."
    )

    sections = [
        f"1) Quick Summary — {summary_sentence}",
        (
            "2) High-Level Design Concept — Recommend a modular or portable ramp setup that spans the single step described as "
            f"'{photo_description}'. If the measured rise is {height}, extend the ramp length to maintain a gentle approach while keeping the door swing ({door_swing}) clear. "
            f"Note reported site constraints: {site_constraints}. Include a stable landing area at the threshold and add temporary edging or rails to guide users. Emphasize that this is a temporary, non-structural aid subject to on-site verification and professional review."
        ),
        "3) Volunteer Materials & Tools (conceptual) — " + "; ".join(materials_lines) + ".",
        "4) Volunteer Task Checklist — " + " ".join(checklist_lines),
        "5) Safety & Permit Notes — " + " ".join(safety_notes),
        "6) Local Resources & Contacts (types) — " + " ".join(resources_lines),
        f"7) Budget Estimate — {budget_section} {budget_comment}",
        f"8) Closing guidance — {closing_guidance}",
    ]

    return "\n".join(sections)


def main() -> int:
    request_text = sys.stdin.read()
    if not request_text.strip():
        print("No input provided.")
        return 1
    context = parse_context(request_text)
    missing = missing_required_fields(context)
    if missing:
        missing_list = ", ".join(missing)
        print(f"Please provide the following before a plan can be drafted: {missing_list}.")
        return 0
    plan = format_plan(context)
    print(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
