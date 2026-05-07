import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Problem, Submission
from runner import run_check50
from mentor import ask_mentor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default-dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AUTH ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
            
        new_user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            name=name
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- UI ROUTES ---

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    submissions = Submission.query.filter_by(user_id=current_user.id).order_by(Submission.submitted_at.desc()).all()
    # Basic stats
    attempted = len(set(s.problem_id for s in submissions))
    solved = len(set(s.problem_id for s in submissions if s.passed))
    return render_template('dashboard.html', submissions=submissions, attempted=attempted, solved=solved)

@app.route('/courses')
@login_required
def courses_api():
    # Return basic course list for React frontend
    return jsonify([
        {'id': 'cs50p', 'title': 'CS50 Python'},
        {'id': 'cs50ai', 'title': 'CS50 AI'}
    ])

@app.route('/courses/<course_id>/lectures')
@login_required
def course_lectures(course_id):
    # Determine distinct lectures for a given course
    problems = Problem.query.filter_by(course=course_id).all()
    lectures = list(set([p.lecture_id for p in problems]))
    lectures.sort()
    return jsonify(lectures)

@app.route('/course/<course_id>')
@login_required
def course_view(course_id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(BASE_DIR, 'content', course_id)
    lectures = []
    if os.path.exists(content_dir):
        for d in os.listdir(content_dir):
            if d.startswith('lecture_'):
                try:
                    num = int(d.split('_')[1])
                except ValueError:
                    continue
                notes_path = os.path.join(content_dir, d, 'notes.md')
                title = f"Lecture {num}"
                if os.path.exists(notes_path):
                    with open(notes_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('# '):
                            title = first_line.replace('# ', '')
                lectures.append({'id': d, 'number': num, 'title': title})
    lectures.sort(key=lambda x: x['number'])
    return render_template('course.html', course_id=course_id, lectures=lectures)

@app.route('/lecture/<course_id>/<lecture_id>')
@login_required
def lecture_view(course_id, lecture_id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    notes_path = os.path.join(BASE_DIR, 'content', course_id, lecture_id, 'notes.md')
    notes_content = ''
    if os.path.exists(notes_path):
        with open(notes_path, 'r', encoding='utf-8') as f:
            notes_content = f.read()
            
    # Also pass problems so we don't need a separate API call if we follow the same pattern
    problems = Problem.query.filter_by(course=course_id, lecture_id=lecture_id).all()
    problems_data = [
        {
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'difficulty': p.difficulty
        } for p in problems
    ]
    return render_template('lecture.html', course_id=course_id, lecture_id=lecture_id, notes=notes_content, problems=problems_data)

@app.route('/api/lecture_data/<course_id>/<lecture_id>')
@login_required
def lecture_data(course_id, lecture_id):
    # Keep this API route in case it's still needed, but the main page will use template vars
    problems = Problem.query.filter_by(course=course_id, lecture_id=lecture_id).all()
    problems_data = [
        {
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'difficulty': p.difficulty
        } for p in problems
    ]
    
    notes = ""
    notes_path = os.path.join('content', course_id, lecture_id, 'notes.md')
    if os.path.exists(notes_path):
        with open(notes_path, 'r', encoding='utf-8') as f:
            notes = f.read()
            
    return jsonify({
        'notes': notes,
        'problems': problems_data
    })

@app.route('/problem/<course_id>/<lecture_id>/<problem_slug>')
@login_required
def problem_view(course_id, lecture_id, problem_slug):
    problem = Problem.query.filter_by(course=course_id, lecture_id=lecture_id, slug=problem_slug).first_or_404()
    problem_data = {
        'id': problem.id,
        'title': problem.title,
        'description': problem.description,
        'course': problem.course,
        'lecture_id': problem.lecture_id,
        'slug': problem.slug,
        'difficulty': problem.difficulty
    }
    return render_template('problem.html', problem=problem_data)

@app.route('/api/problem_data/<int:problem_id>')
@login_required
def problem_data(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    return jsonify({
        'id': problem.id,
        'title': problem.title,
        'description': problem.description,
        'course': problem.course,
        'lecture_id': problem.lecture_id,
        'slug': problem.slug,
        'difficulty': problem.difficulty
    })

# --- API ROUTES ---

@app.route('/submit', methods=['POST'])
@login_required
def submit_code():
    data = request.json
    problem_id = data.get('problem_id')
    code = data.get('code')
    
    problem = Problem.query.get_or_404(problem_id)
    
    # Run check50
    result = run_check50(code, problem.check50_slug)
    
    # Save submission
    sub = Submission(
        user_id=current_user.id,
        problem_id=problem.id,
        code=code,
        passed=result['passed'],
        tests_passed=result['tests_passed'],
        tests_failed=result['tests_failed'],
        raw_output=result['raw_output']
    )
    db.session.add(sub)
    db.session.commit()
    
    return jsonify({
        'status': 'pass' if result['passed'] else 'fail',
        'tests_passed': result['tests_passed'],
        'tests_failed': result['tests_failed'],
        'raw_output': result['raw_output'],
        'submission_id': sub.id
    })

@app.route('/mentor', methods=['POST'])
@login_required
def mentor_chat():
    data = request.json
    problem_id = data.get('problem_id')
    student_message = data.get('student_message', '')
    submission_data = data.get('submission')
    
    problem = Problem.query.get_or_404(problem_id)
    
    # Build student context
    student_context = {
        'id': current_user.id,
        'name': current_user.name
    }
    
    # Get previous attempts
    attempts = Submission.query.filter_by(user_id=current_user.id, problem_id=problem.id).count()
    student_context['attempt_count'] = attempts
    
    # Get completed problems
    completed_subs = Submission.query.filter_by(user_id=current_user.id, passed=True).all()
    completed_ids = set([s.problem_id for s in completed_subs])
    completed_problems = []
    for pid in completed_ids:
        p = Problem.query.get(pid)
        if p:
            completed_problems.append(p.title)
    student_context['completed_problems'] = completed_problems
    
    problem_dict = {
        'title': problem.title,
        'course': problem.course,
        'description': problem.description,
        'check50_slug': problem.check50_slug,
        'common_mistakes': problem.common_mistakes
    }
    
    # Ask mentor
    mentor_reply = ask_mentor(student_context, problem_dict, student_message, submission_data)
    
    return jsonify({
        'mentor_reply': mentor_reply
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
