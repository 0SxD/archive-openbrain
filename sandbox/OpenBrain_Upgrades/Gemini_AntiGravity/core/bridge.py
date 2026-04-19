import os
from litellm import completion
from typing import Optional

def dispatch_agent(role: str, prompt: str, task_type: Optional[str] = None) -> str:
    """
    Universal Model Router utilizing LiteLLM.
    Routes the execution to specific models based on role and task constraints.
    """
    model = ""
    system_instruction = ""
    
    # --- ROUTING LOGIC ---
    if role.lower() == "teacher":
        # Heavy Orchestration
        model = "claude-3-5-sonnet-20241022"
        system_instruction = (
            "You are the OpenBrain Orchestrator. Your role is to govern, evaluate, and provide architecture grading. "
            "Output must strictly follow zero-trust architectural parameters."
        )
        
    elif role.lower() == "student":
        if task_type == "coding":
            # DeepSeek V3 for complex code synthesis
            model = "deepinfra/deepseek-ai/DeepSeek-V3"
            system_instruction = (
                "You are the Developer. You execute the exact requirements of the TDD Rubric without hallucinating features."
            )
        elif task_type == "syntax_check":
            # Groq Llama3 for sub-cent fast validation
            model = "groq/llama3-8b-8192"
            system_instruction = (
                "You are the Grader. Analyze the following code strictly for syntax errors, compile failures, or missing imports. "
                "Output MUST START WITH 'PASS' or 'FAIL'. Do not explain."
            )
        else:
            raise ValueError("Student role requires a valid task_type ('coding' or 'syntax_check')")
            
    else:
        raise ValueError(f"Unknown role identifier: {role}")
        
    # --- EXECUTION ---
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt}
    ]
    
    # Using LiteLLM completion loop to abstract provider endpoints
    try:
        response = completion(
            model=model,
            messages=messages,
            temperature=0.2 if task_type == "coding" else 0.0,
            max_tokens=4000
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"[LITELLM BRIDGE ERROR] Dispatch to {model} failed: {str(e)}"
