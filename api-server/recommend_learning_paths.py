from flask.json import jsonify
import pandas as pd
import numpy as np

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
            if skill not in user_skills and skill not in require_skills:
                item['additional_gain'] = item['additional_gain'] + 1
    
    for item in path:
        item['total'] = alpha * item['occupation_gain'] + beta * item['user_gain'] \
                        + (1 - alpha - beta) * item['additional_gain']

    path = sorted(path, key=get_weight, reverse=True)
    if len(path) > 0:
        return [path[0]]
    else:
        return []