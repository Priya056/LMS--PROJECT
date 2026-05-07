import subprocess
import os
import tempfile
import shutil
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSIONS_DIR = os.path.join(BASE_DIR, 'submissions')
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)


def parse_check50_output(raw_output: str) -> dict:
    """
    Parses raw check50 terminal output to extract pass/fail counts.
    Does NOT strip the raw output — the anti-gravity needs it verbatim.
    """
    passed = len(re.findall(r':sparkles:|:tada:|:checkered_flag:|✅|\\\\\\\) ', raw_output))
    failed = len(re.findall(r':x:|❌|\\\\\\\( ', raw_output))

    # Simpler fallback: count :) and :( in plain text output
    plain_passed = raw_output.count(':)')
    plain_failed = raw_output.count(':(')

    return {
        'tests_passed': max(passed, plain_passed),
        'tests_failed': max(failed, plain_failed)
    }


def run_check50(code: str, check50_slug: str) -> dict:
    """
    Saves student code to submissions/, runs check50, returns full result.

    Returns:
        {
            'passed': bool,
            'tests_passed': int,
            'tests_failed': int,
            'raw_output': str     ← DO NOT OMIT. The anti-gravity needs this.
        }
    """
    tmp_dir = tempfile.mkdtemp(dir=SUBMISSIONS_DIR)
    try:
        code_file = os.path.join(tmp_dir, 'solution.py')
        with open(code_file, 'w') as f:
            f.write(code)

        result = subprocess.run(
            ['check50', '--local', check50_slug, 'solution.py'],
            cwd=tmp_dir,
            capture_output=True,
            text=True,
            timeout=15
        )

        raw_output = result.stdout + result.stderr
        passed = result.returncode == 0
        counts = parse_check50_output(raw_output)

        return {
            'passed': passed,
            'tests_passed': counts['tests_passed'],
            'tests_failed': counts['tests_failed'],
            'raw_output': raw_output or 'check50 produced no output.'
        }

    except subprocess.TimeoutExpired:
        return {
            'passed': False,
            'tests_passed': 0,
            'tests_failed': 0,
            'raw_output': 'Error: Code timed out (>15s). Check for infinite loops.'
        }
    except Exception as e:
        return {
            'passed': False,
            'tests_passed': 0,
            'tests_failed': 0,
            'raw_output': f'Error running check50: {str(e)}'
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
