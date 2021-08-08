from recommend_learning_paths import calculateWeight, filterLearningPaths, search_skill
from flask import Flask, json
from flask import jsonify
from flask import request
from owlready2 import *
from career_path_finding import find_career_path_by_user
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
import csv

# Connect to ontology
path = "file://C:/Users/ndcuo/Downloads/career-counseling-chatbot/career-counseling-chatbot/CareerCounselingOntology.owl"
path = "file://D:/thesis report/data/ITCareerOntology.owl"
path = "file://D:/thesis report/data/TestOntology_20210727.owl"
career_onto = get_ontology(path).load()

cred = credentials.Certificate('it-career-bot-firebase-adminsdk-kyvys-870e6b3f02.json')

app = Flask(__name__)
CORS(app)

default_app = initialize_app(cred)
db = firestore.client()
auth_ref = db.collection('Authentication')
skills_ref = db.collection('JobSpecificSkill')

@app.route('/')
def hello():
    return "You are connecting to Career Counseling server."

@app.route('/api/learning_paths/<occupation>')
def get_job_specific_skills(occupation):
    params = request.get_json()
    duration = None
    if not params['duration'] is None:
        duration = int(params['duration'])
    unit = params['unit']
    target_occupation = career_onto.search(occupation_name=occupation, _case_sensitive=False)
    learning_paths = []

    if len(target_occupation) <= 0:
        return jsonify([]), 200

    # Get all learning paths of target occupation
    for item in target_occupation[0].hasLearningPath:
        learning_path = {
            "learning_path_id": item.learning_path_id[0],
            "courses": [],
            "skills": [],
            "duration": 0,
            "occupation_gain": 0,
            "user_gain": 0,
            "additional_gain": 0,
            "total": 0
        }

        for course in item.hasCourse:
            course_item = {
                'course_id': course.course_id[0],
                'course_name': course.course_name[0],
                'course_description': course.course_description[0],
                'course_url': course.course_url[0],
                'course_duration': course.course_duration[0],
                'skills': []
            }

            learning_path['duration'] = learning_path['duration'] + \
                            int(course.course_duration[0].split(" ")[0])

            for skill in course.provideSkill:
                if skill.skill_id[0] not in learning_path['skills']:
                    learning_path['skills'].append(skill.skill_id[0])
                course_item['skills'].append(skill.skill_name[0])

            learning_path['courses'].append(course_item)
        learning_paths.append(learning_path)

    # Get all require skills of occupation
    require_skills = []
    for skills in target_occupation[0].requireSkill:
        require_skills.append(skills.skill_id[0])

    # Get user's skills
    user_skills = []
    user = career_onto.search(user_id=params['user_id'])
    for skills in user[0].hasSkill:
        user_skills.append(skills.skill_id[0])
    
    # Only select learning paths that have duration less than a value
    print(len(learning_paths))
    learning_paths = filterLearningPaths(learning_paths, duration, unit)
    # Calculate and rank weight of learning paths
    print(len(learning_paths))
    learning_paths = calculateWeight(require_skills, learning_paths, user_skills, 0.4, 0.3)
    return jsonify(learning_paths), 200


@app.route('/api/courses')
def get_course():
    res = []
    courses = list(career_onto.search(type=career_onto.Course))
    for i, item in enumerate(courses):
        res.append({
            'course_id': 'CS10' + str(i),
            'course_name': item.course_name[0]
        })
    return jsonify(res)

@app.route('/api/learning_path/<learning_path_id>/<course_index>')
def get_course_of_learning_path(learning_path_id, course_index):
    path = career_onto.search(learning_path_id=learning_path_id)[0]
    course_index = int(course_index)

    if course_index >= len(path.hasCourse):
        return {}, 400

    course = career_onto.search(course_id=path.hasCourse[course_index].course_id[0])
    res = {}
    res['course_id'] = course[0].course_id[0]
    res['course_name'] = course[0].course_name[0]
    res['duration'] = course[0].course_duration[0]
    res['description'] = course[0].course_description[0]
    res['url'] = course[0].course_url[0]
    res['skills'] = []
    for skill in course[0].provideSkill:
        res['skills'].append(skill.skill_name[0])

    return res, 200

@app.route('/api/courses/<course_id>')
def get_course_detail(course_id):
    res = {}
    courses = list(career_onto.search(type=career_onto.Course, course_id=course_id))
    res['course_id'] = courses[0].course_id[0]
    res['course_name'] = courses[0].course_name[0]
    res['duration'] = courses[0].course_duration[0]
    res['description'] = courses[0].course_description[0]
    res['url'] = courses[0].course_url[0]
    return res, 200

@app.route('/api/courses/<course_id>/skills')
def get_skill_of_course(course_id):
    res = []
    courses = list(career_onto.search(type=career_onto.Course, course_id=course_id))[0]
    for item in courses.provideSkill:
        res.append(item.skill_name[0])
    return jsonify(res), 200

@app.route('/api/user/skills', methods = ['POST'])
def update_skill_of_user():
    params = request.get_json()
    user_id = params['user_id']
    user_skills = params['user_skills']
    current_user = career_onto.search(user_id=user_id)[0]
    current_user.hasSkill = []
    for skill in user_skills:
        item = search_skill(career_onto, skill)
        current_user.hasSkill.append(item)
    
    current_user = career_onto.search(user_id=user_id)[0]
    print(current_user.hasSkill)
    # career_onto.save(path)
    # career_onto = get_ontology(path).load()

    return {}, 200

@app.route('/api/<user_id>/skills')
def get_user_skills(user_id):
    res = []
    user = career_onto.search(user_id=user_id)[0]
    for item in user.hasSkill:
        res.append({
            'skill_id': item.skill_id[0],
            'skill_name': item.skill_name[0]
        })
    return jsonify(res), 200

@app.route("/api/login", methods = ['POST'])
def loginHandler():
    username = request.json['username']
    password = request.json['password']
    users = auth_ref.where('username', '==', username)\
                    .where('password', '==', password)\
                    .stream()
    users = list(users)
    if len(users) <= 0:
        return jsonify({}), 401
    else:
        current_user = users[0]
        data = current_user.to_dict()
        return jsonify({
            'id': current_user.id,
            'name': data['full_name'].split(" ")[-1]
        }), 200


@app.route("/api/skills", methods = ['GET'])
def skillHandler():
    result = []
    search_params = [
        {"type": career_onto.Technology, "text": 'Technology'},
        {"type": career_onto.TechnicalSkill, "text": 'TechnicalSkill'},
        {"type": career_onto.Knowledge, "text": 'Knowledge'}
    ]
    for param in search_params:
        skills = career_onto.search(type=param["type"])
        for item in skills:
            result.append({
                "id": item.skill_id[0],
                "name": item.skill_name[0],
                "type": param["text"]
            })

    return jsonify(result), 200


@app.route("/api/skills/update", methods=['GET'])
def updateSkillHandler():
    auto_id = 1
    with open('skills.csv', 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            skills_ref.document(str(auto_id)).set({
                "id": auto_id,
                "name": row[0],
                "type": row[1]
            })
            auto_id = auto_id + 1

        return {}, 200

if __name__ == '__main__':
    app.run(debug=True)
