import subprocess
from typing import Tuple

def execute_command(command: str, cwd: str = ".") -> Tuple[str, str, int]:
    """
    Agent-Computer Interface (ACI) Ground Truth execution wrapper.
    Pirated from SWE-agent structure. Executes command and strictly captures all standard streams.
    
    Args:
        command (str): the bash or python command string to execute
        cwd (str): the working directory for execution
        
    Returns:
        Tuple containing (stdout string, stderr string, integer exit code)
    """
    try:
        # Use shell=True for complex bash execution equivalent but securely constrained locally
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=30 # Hard 30s timeout to prevent hanging student loops
        )
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired as e:
        return "", f"EXECUTION TIMEOUT EXCEEDED: {e}", 124
    except Exception as e:
        return "", f"EXECUTION FAILED: {str(e)}", 1
