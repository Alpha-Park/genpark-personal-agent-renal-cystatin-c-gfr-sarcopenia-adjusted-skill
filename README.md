# Cystatin-C & Creatinine CKD-EPI Sarcopenia-Adjusted eGFR Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `calculate_sarcopenia_adjusted_egfr`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates combined 2021 CKD-EPI Creatinine-Cystatin C equation, computes Sarcopenia Index (Creatinine / Cystatin C ratio), and removes muscle-mass bias from kidney longevity scores.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Renal Longevity & Sarcopenia)`

## MCP Tool Specification
### `calculate_sarcopenia_adjusted_egfr`
Parameters:
- `serum_creatinine_mg_dl` (float): Serum creatinine in mg/dL
- `serum_cystatin_c_mg_l` (float): Serum Cystatin C in mg/L
- `age_years` (float): Age of patient in years
- `is_female` (bool): Biological sex

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-renal-cystatin-c-gfr-sarcopenia-adjusted-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-renal-cystatin-c-gfr-sarcopenia-adjusted-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
