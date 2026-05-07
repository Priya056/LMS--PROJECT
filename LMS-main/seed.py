import os
import json
from app import app
from models import db, Problem

def seed_database():
    with app.app_context():
        db.create_all()
        
        # Remove the global check since we want to add new problems on rerun
        
        content_dir = os.path.join(os.path.dirname(__file__), 'content')
        if not os.path.exists(content_dir):
            print("Content directory not found. Skipping seed.")
            return
            
        for course_id in os.listdir(content_dir):
            course_path = os.path.join(content_dir, course_id)
            if not os.path.isdir(course_path):
                continue
                
            for lecture_id in os.listdir(course_path):
                lecture_path = os.path.join(course_path, lecture_id)
                if not os.path.isdir(lecture_path):
                    continue
                    
                problems_file = os.path.join(lecture_path, 'problems.json')
                if os.path.exists(problems_file):
                    with open(problems_file, 'r', encoding='utf-8') as f:
                        try:
                            problems = json.load(f)
                            for p_data in problems:
                                existing = Problem.query.filter_by(slug=p_data['id'], course=course_id).first()
                                if not existing:
                                    # Serialize common_mistakes to JSON string as required
                                    mistakes = p_data.get('common_mistakes', [])
                                    mistakes_json = json.dumps(mistakes)
                                    
                                    problem = Problem(
                                        course=course_id,
                                        lecture_id=lecture_id,
                                        slug=p_data['id'],
                                        title=p_data['title'],
                                        description=p_data['description'],
                                        check50_slug=p_data['check50_slug'],
                                        difficulty=p_data.get('difficulty', 'medium'),
                                        common_mistakes=mistakes_json
                                    )
                                    db.session.add(problem)
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in {problems_file}")
                            
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_database()
