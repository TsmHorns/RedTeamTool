# RedTeamTool

Utility for generating safety-conscious prompt mutations and simulated responses for red-team evaluation research.

## Usage

```bash
python tool.py "Seed prompt here"
```

The tool outputs a JSON array containing five mutated prompts, corresponding mock responses, exposure scores, reasoning, and optional mitigation guidance when high risk is detected.
