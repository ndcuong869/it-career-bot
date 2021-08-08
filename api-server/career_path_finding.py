import logging
import sys

def find_career_path_by_job(job_role, career_onto):
    career_path = career_onto.search(
        type=career_onto.CareerLearningPath, of_job_role=job_role)
    return career_path


level_dict = {
    'entry level': 1,
    'mid level': 2,
    'senior level': 3,
    'professional level': 4
}

def sort_level(level):
    return level_dict[level]


def find_career_path_level(career_path):
    levels = []
    for item in career_path:
        if item.has_level[0] not in levels:
            levels.append(item.has_level[0])
    sorted(levels, key=sort_level)
    return levels


def filter_by_level(career_path, selected_level):
    res = []
    for item in career_path:
        if item.has_level[0] == selected_level:
            res.append(item)
    return res

def find_career_path_by_user(user_profile, career_onto):
    print(user_profile.has_career[0], file=sys.stderr)
    job_role = user_profile.has_career[0]
    completed_career_path = user_profile.has_completed_career_paths
    res = []
    career_path = find_career_path_by_job(job_role, career_onto)
    print(career_path, file=sys.stderr)
    if len(completed_career_path) <= 0:
        return filter_by_level(career_path, 'entry level')
    else:
        current_level = find_career_path_level(
            completed_career_path)[0]
        print(current_level, file=sys.stderr)
        levels = find_career_path_level(career_path)
        for i, level in enumerate(levels):
            if current_level == level:
                if i + 1 >= len(levels):
                    return []
                else:
                    filtered_career_path = filter_by_level(career_path, levels[i + 1])
                    return filtered_career_path

        return filter_by_level(career_paths, levels[0])
