# Fraylon Academy — Learning Management System

A minimal, robust, and functional Learning Management System (LMS) built for Fraylon Technologies. This LMS hosts courses (CS50 Python and CS50 AI) and features an embedded AI coding tutor called **Fraylon Mentor (anti-gravity)**. 

The mentor interprets raw `check50` terminal output and student context to provide targeted, Socratic guidance without giving away direct answers.

---

## 🎯 Key Features

- **Single Directory Architecture**: All content, logic, and templates live in a single unified directory. No complex subdomains or isolated microservices.
- **Embedded AI Mentor**: Deep Anthropic API integration (`claude-opus-4-5`) acts as a Socratic tutor, directly reading `check50` raw outputs to guide students to solutions.
- **Automated Test Runner**: Uses `check50` under the hood to run tests on student code inside isolated temporary directories.
- **Progress Tracking**: Built-in Dashboard displaying attempt counts, solved problems, and detailed submission histories.
- **React Frontend via CDN**: Preserves the single-directory structure by compiling modern React/JSX components directly in the browser via Babel, avoiding complex Node/Webpack pipelines.
- **Markdown Lecture Rendering**: Lecture notes automatically parsed and rendered natively in the browser.

---

## 📂 Directory Structure

```text
fraylon_lms/
├── app.py                      # Main Flask application and API routes
├── models.py                   # SQLAlchemy Database models (User, Problem, Submission)
├── runner.py                   # Wrapper executing check50 in isolated temp dirs
├── mentor.py                   # Anthropic API wrapper handling Fraylon Mentor logic
├── mentor_system_prompt.txt    # Socratic tutor instructions for the Mentor
├── seed.py                     # Database initialization script
├── requirements.txt            # Python dependencies
├── content/                    # Markdown notes and problem definitions (JSON)
│   ├── cs50p/
│   └── cs50ai/
├── templates/                  # HTML and embedded React JSX components
└── static/                     # Minimal flat dark CSS styling
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- **Linux / macOS / WSL**: `check50` is a UNIX-based tool. Natively running `check50` on Windows will fail. Use WSL for local development or deploy to a Linux environment (e.g., Render.com).

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
You MUST set the required environment variables before running the application or the Fraylon Mentor will fail to initialize.

```bash
# macOS / Linux / WSL
export ANTHROPIC_API_KEY="sk-ant-your-api-key"
export FLASK_SECRET_KEY="fraylon-secret"

# Windows PowerShell (Not recommended for runner.py execution, but works for the server)
$env:ANTHROPIC_API_KEY="sk-ant-your-api-key"
$env:FLASK_SECRET_KEY="fraylon-secret"
```

### 3. Seed the Database
Initialize the SQLite database and populate it with the CS50p and CS50ai problems from the `content/` directory.
```bash
python seed.py
```
*(Note: `seed.py` is idempotent. Running it multiple times will safely skip duplicate problem entries.)*

---

## 💻 Execution

Start the Flask development server:
```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

### Testing locally on Windows without WSL
If you are running the Flask app directly on Windows, the `runner.py` subprocess call to `check50` will fail. The app will catch the error and display it gracefully in the frontend, allowing you to test the UI and chat layout, but test results will not pass. For complete end-to-end functionality, either run the stack inside WSL, or deploy to a Linux container.

---

## 🧠 The Fraylon Mentor (anti-gravity)

The Fraylon Mentor is configured to:
- Never provide direct solutions.
- Read and interpret `check50` test failures.
- Provide guidance based on pre-defined `common_mistakes` found in `problems.json`.
- Maintain a session context including previous student attempts and completed problems.

The mentor's prompt can be modified directly in `mentor_system_prompt.txt`.

---

*Fraylon Technologies · Internal Use Only · May 2026*