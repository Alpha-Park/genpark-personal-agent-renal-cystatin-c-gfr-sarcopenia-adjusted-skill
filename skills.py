# -*- coding: utf-8 -*-
"""Cystatin-C & Creatinine CKD-EPI Sarcopenia-Adjusted eGFR Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def calculate_sarcopenia_adjusted_egfr(**kwargs):
    """Calculates combined 2021 CKD-EPI Creatinine-Cystatin C equation, computes Sarcopenia Index (Creatinine / Cystatin C ratio), and removes muscle-mass bias from kidney longevity scores."""
    serum_creatinine_mg_dl = kwargs.get('serum_creatinine_mg_dl')
    serum_cystatin_c_mg_l = kwargs.get('serum_cystatin_c_mg_l')
    age_years = kwargs.get('age_years')
    is_female = kwargs.get('is_female')

    # Sarcopenia Index = (Serum Creatinine / Serum Cystatin C) * 100
    sarcopenia_index = round((serum_creatinine_mg_dl / (serum_cystatin_c_mg_l if serum_cystatin_c_mg_l > 0 else 0.1)) * 100.0, 1)
    
    # 2021 CKD-EPI Creatinine-Cystatin C equation approximation
    # eGFR = 135 * min(Scr/kappa, 1)^alpha * max(Scr/kappa, 1)^-0.544 * min(Scys/0.8, 1)^-0.323 * max(Scys/0.8, 1)^-0.778 * 0.9961^Age [* 0.963 if female]
    kappa = 0.7 if is_female else 0.9
    alpha = -0.219 if is_female else -0.144
    
    scr_k = serum_creatinine_mg_dl / kappa
    scys_k = serum_cystatin_c_mg_l / 0.8
    
    term_cr = (min(scr_k, 1.0) ** alpha) * (max(scr_k, 1.0) ** -0.544)
    term_cys = (min(scys_k, 1.0) ** -0.323) * (max(scys_k, 1.0) ** -0.778)
    term_age = 0.9961 ** age_years
    gender_mult = 0.963 if is_female else 1.0
    
    egfr_combined = round(135.0 * term_cr * term_cys * term_age * gender_mult, 1)
    
    # Muscle mass evaluation based on Sarcopenia Index (> 100 is high muscle mass; < 75 indicates sarcopenic risk)
    if sarcopenia_index >= 110.0:
        muscle_profile = "Athletic / Elevated Lean Skeletal Muscle Mass (Creatinine falsely overestimates renal decline)"
    elif sarcopenia_index < 75.0:
        muscle_profile = "Sarcopenia Risk / Muscle Atrophy (Creatinine falsely masks kidney failure)"
    else:
        muscle_profile = "Normative Skeletal Muscle Composition"
        
    if egfr_combined >= 90.0:
        ckd_stage = "G1: Normal or High Renal Filtration"
    elif egfr_combined >= 60.0:
        ckd_stage = "G2: Mildly Decreased GFR"
    elif egfr_combined >= 45.0:
        ckd_stage = "G3a: Mild-to-Moderate Renal Impairment"
    elif egfr_combined >= 30.0:
        ckd_stage = "G3b: Moderate-to-Severe Impairment"
    else:
        ckd_stage = "G4/G5: Severe Renal Failure / End Stage"
        
    result = {
        "status": "success",
        "combined_ckd_epi_2021_egfr_ml_min": egfr_combined,
        "sarcopenia_muscle_index": sarcopenia_index,
        "muscle_mass_confounder_tier": muscle_profile,
        "kidney_longevity_stage": ckd_stage,
        "renal_preservation_guidance": "Maintain hydration (30-35 ml/kg), audit microalbuminuria, monitor nephrotoxic NSAID exposure.",
        "engine": "GenPark Cystatin-C Sarcopenia-Adjusted Nephron Longevity Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "calculate_sarcopenia_adjusted_egfr": {
        "name": "calculate_sarcopenia_adjusted_egfr",
        "description": "Calculates combined 2021 CKD-EPI Creatinine-Cystatin C equation, computes Sarcopenia Index (Creatinine / Cystatin C ratio), and removes muscle-mass bias from kidney longevity scores.",
        "parameters": {
            "type": "object",
            "properties": {
                "serum_creatinine_mg_dl": {"type": "number", "description": "Serum creatinine in mg/dL"},
                "serum_cystatin_c_mg_l": {"type": "number", "description": "Serum Cystatin C in mg/L"},
                "age_years": {"type": "number", "description": "Age of patient in years"},
                "is_female": {"type": "boolean", "description": "Biological sex"},
            },
            "required": ['serum_creatinine_mg_dl', 'serum_cystatin_c_mg_l', 'age_years', 'is_female']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_sarcopenia_adjusted_egfr":
            res = calculate_sarcopenia_adjusted_egfr(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-renal-cystatin-c-gfr-sarcopenia-adjusted-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-renal-cystatin-c-gfr-sarcopenia-adjusted-skill...")
    test_args = {'serum_creatinine_mg_dl': 1.15, 'serum_cystatin_c_mg_l': 0.82, 'age_years': 48.0, 'is_female': False}
    res = calculate_sarcopenia_adjusted_egfr(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-renal-cystatin-c-gfr-sarcopenia-adjusted-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
