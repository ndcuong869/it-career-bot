# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import urllib
import requests
import logging
import webbrowser

from requests.api import request

logger = logging.Logger(__name__)
root_url = "http://localhost:3000"

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionOpenLoginPage(Action):
    def name(self) -> Text:
        return "action_open_login_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = root_url + '/login'
        webbrowser.register('edge',
                            None,
                            webbrowser.BackgroundBrowser("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
        webbrowser.get('edge').open_new(url)
        return []


class ActionOpenChatbotSurvey(Action):
    def name(self) -> Text:
        return "action_open_chatbot_survey"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'bit.ly/it_career_bot_survey'
        webbrowser.register('edge',
                            None,
                            webbrowser.BackgroundBrowser("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
        webbrowser.get('edge').open_new(url)
        return []

class ActionOpenRegisterPage(Action):
    def name(self) -> Text:
        return "action_open_register_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = root_url + '/register'
        webbrowser.register('edge',
                            None,
                            webbrowser.BackgroundBrowser("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
        webbrowser.get('edge').open_new(url)
        return []

class ActionGreeting(Action):
    def name(self) -> Text:
        return "action_greeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='Hi')
        dispatcher.utter_message(text='I am a career counseling bot powered by FIT-HCMUS. ')
        dispatcher.utter_message(text='Firstly, you should login or register in below.', buttons = [
                {"title": "Login now", "payload": "/open_login_page"},
                {"title": "Register now", "payload": "/open_register_page"}
            ])

        return []

class ActionGreetingWithName(Action):
    def name(self) -> Text:
        return "action_greeting_with_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot('user_name')
        dispatcher.utter_message(text='Hello {0}'.format(user_name))
        dispatcher.utter_message(text='I can help you find the best learning path for your career development.')
        dispatcher.utter_message(text='What is your dream job?')

        return []

class ActionOpenUserSkillPage(Action):
    def name(self) -> Text:
        return "action_open_user_skill_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.get_slot("user_id")
        url = root_url + '/user/skills'
        webbrowser.register('edge',
                            None,
                            webbrowser.BackgroundBrowser("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
        webbrowser.get('edge').open_new(url)
        return []

class ActionHandleUpdateUserSkill(Action):
    def name(self) -> Text:
        return "action_handle_update_user_skill"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_skills = tracker.get_slot('user_skill')
        print(len(user_skills))
        
        user_id = tracker.get_slot("user_id")
        url_user = 'http://127.0.0.1:5000/api/' + user_id + '/skills'
        response = requests.get(url_user)
        new_user_skills = response.json()
        print(len(new_user_skills))

        if len(new_user_skills) > len(user_skills):
            dispatcher.utter_message("You have updated from {0} skills to {1} skills.".format(len(user_skills), len(new_user_skills)))
            dispatcher.utter_message("Do you continue to find the best learning paths with these skills?")

        return []

class ActionCareerQuestionHandler(Action):
    def name(self) -> Text:
        return "action_career_question_handler"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        main_career = tracker.get_slot("main_career")
        job_role = main_career
        career_position = ""
        platform = ""
        unit = None
        for item in tracker.latest_message['entities']:
                if item['entity'] == 'duration':
                    unit = item['additional_info']['unit']

        if main_career == 'developer':
            for item in tracker.latest_message['entities']:
                if item['entity'] == 'career_position':
                    career_position = item['value']
                if item['entity'] == 'platform':
                    platform = item['value']
            job_role = career_position + " " + platform + " " + main_career

        user_id = tracker.get_slot("user_id")
        url_user = 'http://127.0.0.1:5000/api/' + user_id + '/skills'
        response = requests.get(url_user)
        user_skills = response.json()

        dispatcher.utter_message(text='I know that you want to become a {0}. '.format(job_role))
        # dispatcher.utter_message(text='To give the best recommendation for you, I need to know your skills. ')
        dispatcher.utter_message(text='To give the best recommendation for you, I need to understand your strengs and abilities. ')
        dispatcher.utter_message(text='I found that you have learned {0} skills before.'.format(len(user_skills)))
        dispatcher.utter_message(text='Do you want to continue with these skills?', buttons=[
            {"title": "Manage skills", "payload": "/open_user_skill_page"},
        ])

        return [SlotSet("job_role", job_role), SlotSet("duration_unit", unit), SlotSet("user_skill", user_skills)]


class ActionConfirmSkillInput(Action):
    def name(self) -> Text:
        return "action_confirm_skill_input"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message('Do you want to add new skills?')
        return []


class ActionFindCareerPath(Action):
    def name(self) -> Text:
        return "action_find_career_path"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        job_role = tracker.get_slot('job_role')
        user_id = tracker.get_slot('user_id')
        duration = tracker.get_slot('duration')
        duration_unit = tracker.get_slot('duration_unit')
        while "  " in job_role:
            job_role = job_role.replace("  ", " ")
        
        url = 'http://127.0.0.1:5000/api/learning_paths/' + job_role
        data = {
            'user_id': user_id,
            'duration': duration,
            'unit': duration_unit
        }
        response = requests.get(url, json=data)
        paths = response.json()

        url_user = 'http://127.0.0.1:5000/api/' + user_id + '/skills'
        response = requests.get(url_user)
        user_skills = response.json()

        user_skills_str = ""
        for item in user_skills:
            user_skills_str = user_skills_str + " " + item['skill_name'] + ", "
        user_skills_str = user_skills_str[0:len(user_skills_str) - 2]

        if len(paths) <= 0:
            dispatcher.utter_message('Let me see...')
            dispatcher.utter_message('We don\'t have any career paths to become {0}.'
                                     'You can find in the next time.'.format(job_role))
            return []
        else:
            dispatcher.utter_message('Let me see… ')
            # dispatcher.utter_message("I know that you have learned {0}."\
            #                             .format(user_skills_str))
            dispatcher.utter_message('The best learning paths for your'
                                    ' career consist of {0} courses. '\
                                    .format(len(paths[0]['courses']))) 

            for index, item in enumerate(paths[0]['courses']):
                dispatcher.utter_message('Course {0}: {1}'.format(index + 1, item['course_name']))
            learning_path_id = paths[0]['learning_path_id']

            duration = int(paths[0]['duration'])
            dispatcher.utter_message('You take {0} hours to complete this learning path.'.format(duration))
            dispatcher.utter_message('If you spend 3 hours each week to learn, you will complete this learning path in {0} months'.format(int((duration / 12))))
            dispatcher.utter_message('Do you want to know about a course detail?')

            return [SlotSet("learning_path_id", learning_path_id)]
        


class ActionViewCourseDetail(Action):
    def name(self) -> Text:
        return "action_view_course_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_index = ""
        for item in tracker.latest_message['entities']:
            if item['entity'] == 'course':
                course_index = item['value'].split(" ")[1]
        learning_path_id = tracker.get_slot("learning_path_id")
        response = requests.get("http://127.0.0.1:5000/api/learning_path/" + learning_path_id + "/" + str(int(course_index) - 1))
        if response.status_code == 400:
            dispatcher.utter_message("The course index is invalid. Please try another.")
        else:
            data = response.json()
            skill_str = ""
            for skill in data['skills']:
                skill_str = skill_str + skill + ", "
            skill_str = skill_str[0:len(skill_str) - 2]
            dispatcher.utter_message(text="Course {0}: {1}".format(course_index, data['course_name']))
            dispatcher.utter_message(text="Description: {0}".format(data['description']))
            dispatcher.utter_message(text="You take {0} to complete this course.".format(data['duration']))
            duration = int(int(data['duration'].split(" ")[0]) / (3 * 4))
            dispatcher.utter_message(text="If you spend 3 hours each week to learn, you will complete them in {0} months".format(duration))
            dispatcher.utter_message(text="After completing this course, you will have experience in {0}.".format(skill_str))
            dispatcher.utter_message(text="You can access this course by using this url: {0}".format(data['url']))

        return []

class ActionVerifyLogin(Action):
    def name(self) -> Text:
        return "action_verify_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        token = tracker.get_slot('token')
        logging.info(token)
        return []


class ActionProvideSkills(Action):
    def name(self) -> Text:
        return "action_provide_skills"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skill_list = ""
        job_role = tracker.get_slot('job_role')
        for item in tracker.latest_message['entities']:
            if item['entity'] == 'skill':
                skill_list = skill_list + " " + item['value']

        # dispatcher.utter_message(text="You have some experiences in {0}. "
        # "This is great.".format(skill_list))
        # dispatcher.utter_message(text="However, you need to learn some advanced skills to "
        # "become a good {0}.".format(job_role))
        # dispatcher.utter_message(text="I will recommend some courses for you. "
        # "Do you want to see them?")

        dispatcher.utter_message(text='You have some experiences in {0}. '
                                 'This is great. However, you need to learn some advanced skills to '
                                 'become a good {0}. I will recommend some courses for you. '
                                 'Do you want to see them?'.format(job_role)
                                 )

        return []


class ActionConfirmSkill(Action):
    def name(self) -> Text:
        return "action_confirm_skill"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        job_role = tracker.get_slot('job_role')

        response = requests.get(
            "http://127.0.0.1:5000/" + urllib.parse.quote(job_role) + "/skills")
        skill_list = response.json()
        skills = []
        for skill in skill_list:
            skills.append(skill['skill_name'])

        skill_text = ""
        if len(skills) > 1:
            skill_text = skills[0]
            for i in range(1, len(skills) - 1):
                skill_text = skill_text + ", " + skills[i]
            skill_text = skill_text + " and " + skills[len(skills) - 1]
        else:
            skill_text = skills[0]

        dispatcher.utter_message(text="Let me see. To become a {0}, "
                                 "you need to have {1}. Do you want to see courses for them?"
                                 .format(job_role, skill_text))

        return []


class ActionRequireSelectCourses(Action):
    def name(self) -> Text:
        return "action_require_select_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://127.0.0.1:5000")
        logger.debug(response)
        logger.debug(response.json())
        courses = response.json()
        selected_skill = tracker.get_slot("skill")
        dispatcher.utter_message(text="I find {0} courses to learn about {1}. "
                                 "Do you want to see them?".format(
                                     len(courses), selected_skill)
                                 )

        return []


class ActionProvideCourse(Action):
    def name(self) -> Text:
        return "action_provide_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_course = tracker.get_slot("current_course")
        #response = requests.get("http://127.0.0.1:5000/courses/{0}".format(current_course))
        response = requests.get('http://127.0.0.1:5000/courses')
        course = response.json()
        dispatcher.utter_message(
            text="You can learn a course named {0}.".format(course[0]['course_name']))

        return []
