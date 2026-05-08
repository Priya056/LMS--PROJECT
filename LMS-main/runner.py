import subprocess
import os
import tempfile
import shutil
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSIONS_DIR = os.path.join(BASE_DIR, 'submissions')
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)


def parse_pytest_output(raw_output: str) -> dict:
    """
    Parses raw pytest terminal output to extract pass/fail counts.
    Does NOT strip the raw output — the anti-gravity needs it verbatim.
    """
    passed = len(re.findall(r' PASSED', raw_output))
    failed = len(re.findall(r' FAILED', raw_output))

    return {
        'tests_passed': passed,
        'tests_failed': failed
    }


def run_check50(code: str, check50_slug: str) -> dict:
    """
    Saves student code to submissions/, runs pytest against the test file, returns full result.
    Note: Function name is kept as run_check50 for backward compatibility with app.py.
    
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

        # Copy the pytest file to the tmp dir
        test_file_source = os.path.join(BASE_DIR, check50_slug)
        test_file_dest = os.path.join(tmp_dir, os.path.basename(check50_slug))
        if os.path.exists(test_file_source):
            shutil.copy(test_file_source, test_file_dest)
        else:
            return {
                'passed': False,
                'tests_passed': 0,
                'tests_failed': 1,
                'raw_output': f'Error: Test file not found at {check50_slug}'
            }

        result = subprocess.run(
            ['pytest', os.path.basename(check50_slug), '-v'],
            cwd=tmp_dir,
            capture_output=True,
            text=True,
            timeout=15
        )

        raw_output = result.stdout + result.stderr
        passed = result.returncode == 0
        counts = parse_pytest_output(raw_output)

        return {
            'passed': passed,
            'tests_passed': counts['tests_passed'],
            'tests_failed': counts['tests_failed'],
            'raw_output': raw_output or 'pytest produced no output.'
        }

    except subprocess.TimeoutExpired:
        return {
            'passed': False,
            'tests_passed': 0,
            'tests_failed': 0,
            'raw_output': 'Error: Code timed out (>15s). Check for infinite loops or waiting for input().'
        }
    except Exception as e:
        return {
            'passed': False,
            'tests_passed': 0,
            'tests_failed': 0,
            'raw_output': f'Error running pytest: {str(e)}'
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
