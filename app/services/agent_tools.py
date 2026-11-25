import subprocess


ALLOWED_TARGET = "127.0.0.1"
ALLOWED_PORT = "8000"


def run_nmap_scan(target: str) -> dict:
    """
    Run a restricted Nmap scan against the local lab target.
    """

    if target != ALLOWED_TARGET:
        return {
            "executed": False,
            "error": "Target is not allowlisted.",
        }

    command = [
        "nmap",
        "-sT",
        "-T2",
        "-p",
        ALLOWED_PORT,
        ALLOWED_TARGET,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        return {
            "executed": result.returncode == 0,
            "target": ALLOWED_TARGET,
            "port": ALLOWED_PORT,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "simulation_only": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "executed": False,
            "error": "Nmap scan timed out.",
        }
