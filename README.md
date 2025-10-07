# RedTeamTool

Utility for generating safety-conscious prompt mutations and simulated responses for red-team evaluation research.

## Usage

```bash
python tool.py "Seed prompt here"
```

The tool outputs a JSON array containing five mutated prompts, corresponding mock responses, exposure scores, reasoning, and optional mitigation guidance when high risk is detected.

## CivicBuildAssistant prototype

Generate a plain-text temporary ramp planning outline by piping request context into the CivicBuildAssistant utility:

```bash
python civic_build_tool.py <<'EOF'
Location name: Eastwood Community Center
Photo description: single concrete step, about 6 inches high, outward-swinging door with narrow landing
Measured step height: 6
Door swing: outward
Budget level: low
Volunteer skill level: novice
Any site constraints: limited sidewalk space on the right side
EOF
```

If required fields are missing or marked unknown, the tool will request the missing information instead of producing a plan.
