from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
import datetime

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("response-template.html")


def search_skill(onto, skill_name):
    return onto.search(skill_name=skill_name)[0]

def filterLearningPaths(paths, duration, unit):
    if unit == None:
        return paths
    if unit == "week": 
        duration = duration / 4
    if unit == "year":
        duration = duration * 12

    selected_paths = []
    for path in paths:
        path_duration = path["duration"] / (3 * 4)
        if path_duration < duration:
            selected_paths.append(path)
    
    return selected_paths

def get_weight(item):
    return item['total']

def print_response(paths):
    df_paths = pd.DataFrame(paths)
    template_vars = {"title" : "The learning path recommendation",
                 "national_pivot_table": df_paths.to_html(),
                 "created_time": datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
                 }
    html_out = template.render(template_vars)
    with open('my_new_html_file.html', 'w') as f:
        f.write(html_out)

def calculateWeight(require_skills, path, user_skills, alpha, beta):
    if alpha + beta > 1:
        alpha = 0.5
        beta = 0.5

    for skill in require_skills:
        for item in path:
            if skill in item['skills']:
                item['occupation_gain'] = item['occupation_gain'] + 1
    
    for item in path:
        for skill in item['skills']:
            if skill not in user_skills and skill in require_skills:
                item['user_gain'] = item['user_gain'] + 1
                item['gain_skills'].append(skill)
            if skill not in user_skills and skill not in require_skills:
                item['additional_gain'] = item['additional_gain'] + 1
                item['additional_skills'].append(skill)

    # Normalize the paths' weight
    label_list = ['occupation_gain', 'user_gain', 'additional_gain']
    for label in label_list:
        weight = []
        for item in path:
            weight.append(item[label])
        max_weight = max(weight)
        for item in path:
            item[label] = item[label] / max_weight

    for item in path:
        item['total'] = alpha * item['occupation_gain'] + beta * item['user_gain'] \
                        + (1 - alpha - beta) * item['additional_gain']

    path = sorted(path, key=get_weight, reverse=True)

    normal_paths = []
    for item in path:
        normal_paths.append({
            'ID': item['learning_path_id'],
            'skills': item['skills'],
            'duration': item['duration'],
            'occupation_gain': item['occupation_gain'],
            'user_gain': item['user_gain'],
            'additional_gain': item['additional_gain'],
            'weight': item['total']
        })

    if len(path) > 0:
        print_response(normal_paths)
        return path[0:3]
    else:
        return []



