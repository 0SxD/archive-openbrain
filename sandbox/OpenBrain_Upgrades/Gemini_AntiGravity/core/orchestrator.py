import sys
import os
import json
import time
import argparse

# --- ENTRY-001: sys.path injection ---
# Pin import root to this file's directory so sibling modules (bridge, cli_ux,
# execution_engine) resolve correctly regardless of invocation CWD.
# Source: research.md ENTRY-001, https://github.com/python/cpython
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ensure local decoupled modules are accessible
from bridge import dispatch_agent
from cli_ux import render_audit_gate, render_loop_progress, render_rubric_checklist, render_matrix_view
from execution_engine import execute_command

def extract_json(response: str) -> str:
    """Helper to extract JSON strings from markdown block formats."""
    if "```json" in response:
        return response.split("```json")[1].split("```")[0].strip()
    return response.strip()

def load_project_rules(project: str) -> str:
    rules_path = f"../projects/{project}/rules.md"
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            return f.read()
    return "No project-specific rules provided."

def load_teacher_prompt() -> str:
    prompt_path = "../harnesses/openrouter_extreme_loop/prompts/teacher_orchestrator.md"
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def run_extreme_loop(mission_objective: str, project: str, max_iterations: int = 2):
    """
    Module 5: Extreme Loop Orchestrator with ACI
    Manages the Teacher -> Student -> ACI -> Grader circuit.
    """
    project_rules = load_project_rules(project)
    teacher_base_prompt = load_teacher_prompt()
    
    # 1. Teacher generates JSON Rubric
    print(f"\n[ORCHESTRATOR] Initializing Teacher for project: {project}")
    teacher_prompt = (
        f"{teacher_base_prompt}\n\nProject Rules to enforce:\n{project_rules}\n\n"
        f"Generate a strict TDD Evaluation Rubric for the following mission: '{mission_objective}'. "
        f"Return ONLY a JSON object with this schema: "
        f'{{"mission": "string", "criteria": [{{"id": 1, "task": "string", "passed": false}}]}}'
    )
    
    teacher_rubric_raw = dispatch_agent(role="Teacher", prompt=teacher_prompt)
    rubric_json = extract_json(teacher_rubric_raw)
    render_rubric_checklist(rubric_json)
    
    current_code = ""
    iteration = 1
    
    while iteration <= max_iterations:
        render_loop_progress(iteration, max_iterations)
        
        # 2. Student (DeepSeek) writes exactly to the rubric
        print(f"\n[ORCHESTRATOR] Dispatching Student for code generation...")
        coding_prompt = (
            f"Project Rules: {project_rules}\n"
            f"Here is your strict TDD criteria rubric: \n{rubric_json}\n\n"
            f"Write the implementation Python script. Return ONLY raw code."
        )
        current_code = dispatch_agent(role="Student", prompt=coding_prompt, task_type="coding")
        
        # Write to intermediate temp file to run
        temp_file = "sandbox_output.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(current_code.replace("```python", "").replace("```", "").strip())
        
        # 3. ACI Execution
        print(f"\n[ORCHESTRATOR] Running Ground Truth execution via ACI...")
        stdout, stderr, exit_code = execute_command(f"python {temp_file}")
        
        render_matrix_view(current_code, stderr if exit_code != 0 else stdout)
        
        # 4. Grader (Groq) fast-checks syntax/stderr if failure
        if exit_code != 0:
            print(f"\n[ORCHESTRATOR] Submitting ACI Crash to Grader for Syntax correction...")
            sanity_check_prompt = f"The terminal crashed with exit code {exit_code}. Stderr:\n{stderr}\n\nOriginal Code:\n{current_code}"
            syntax_analysis = dispatch_agent(role="Student", prompt=sanity_check_prompt, task_type="syntax_check")
            
            render_audit_gate("SYNTAX GRADER", "FAIL", syntax_analysis)
            iteration += 1
            print("\n[ORCHESTRATOR] Rebounding to student...")
            time.sleep(1)
            continue
            
        render_audit_gate("SYNTAX GRADER", "PASS", "ACI Execution clean. Zero crashes detected.")
        print("\n[ORCHESTRATOR] Code compiled and ran cleanly. Presenting to Teacher for Audit.")
        
        # 5. Teacher Audits the Code against Rubric
        audit_prompt = (
            f"Here is the strict rubric: \n{rubric_json}\n\n"
            f"Here is the working code: \n{current_code}\n\n"
            f"Did it fulfill EVERY criterion and project rule? Start your response with 'PASS' or 'FAIL'. Explain why."
        )
        audit_feedback = dispatch_agent(role="Teacher", prompt=audit_prompt)
        
        if audit_feedback.strip().upper().startswith("PASS"):
            render_audit_gate("FINAL TEACHER AUDIT", "PASS", audit_feedback)
            print("\n[ORCHESTRATOR] Cycle Complete. Code stored.")
            return current_code
        else:
            render_audit_gate("FINAL TEACHER AUDIT", "FAIL", audit_feedback)
            iteration += 1

    render_audit_gate("BOUNDING BOX REACHED", "BLOCK", "Maximum iterations reached. Mission aborted.")
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="openbrain_core", help="Target project silo")
    parser.add_argument("--mission", default="Write a python script that prints Hello World.", help="Mission string")
    args = parser.parse_args()
    
    run_extreme_loop(args.mission, project=args.project)

if __name__ == "__main__":
    main()
