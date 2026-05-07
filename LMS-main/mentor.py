import anthropic
import os
import json

def build_mentor_context(student, problem, submission=None, student_message=""):
    """
    Composes the full message injected into the Fraylon Mentor.
    Format must match the anti-gravity's RUNTIME CONTEXT INJECTION spec exactly.
    """
    
    # Parse common mistakes if it's a JSON string
    common_mistakes = problem.get('common_mistakes', 'Not specified.')
    if isinstance(common_mistakes, str):
        try:
            mistakes_list = json.loads(common_mistakes)
            if isinstance(mistakes_list, list):
                common_mistakes = "\n".join([f"- {m}" for m in mistakes_list])
        except json.JSONDecodeError:
            pass
            
    ctx = f"""=== CURRENT SESSION CONTEXT ===

STUDENT: {student['name']} (ID: {student['id']})

COURSE: {problem['course'].upper()}

CURRENT PROBLEM: {problem['title']}

PROBLEM DESCRIPTION:
{problem['description']}

CHECK50 SLUG: {problem['check50_slug']}

COMMON MISTAKES ON THIS PROBLEM:
{common_mistakes}

"""
    if submission:
        ctx += f"""STUDENT'S CURRENT CODE:
```python
{submission['code']}
```

CHECK50 RESULTS:
- Overall: {"PASSED" if submission['passed'] else "FAILED"}
- Tests passed: {submission.get('tests_passed', 'N/A')}
- Tests failed: {submission.get('tests_failed', 'N/A')}
- Raw output:
{submission['raw_output']}

"""

    ctx += f"STUDENT'S PREVIOUS ATTEMPTS ON THIS PROBLEM: {student.get('attempt_count', 0)}\n"
    completed = student.get('completed_problems', [])
    ctx += f"PROBLEMS COMPLETED SO FAR: {', '.join(completed) if completed else 'None'}\n"
    ctx += "\n=== END CONTEXT ===\n"
    
    if student_message:
        ctx += f"\nStudent message: {student_message}"
        
    return ctx


def ask_mentor(student, problem, student_message, submission=None):
    """
    Calls the Fraylon Mentor (anti-gravity) with properly injected context.
    Returns the mentor's response as a string.
    """
    system_prompt_path = os.path.join(os.path.dirname(__file__), 'mentor_system_prompt.txt')
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    user_message = build_mentor_context(student, problem, submission, student_message)

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response.content[0].text
